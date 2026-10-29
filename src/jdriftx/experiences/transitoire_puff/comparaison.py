"""Comparaison des routes transitoires, assemblage et manifeste (étape 6)."""

from __future__ import annotations

from importlib import metadata

from pydantic import BaseModel, ConfigDict

from jdriftx.benchmarks.cas import PointMesure
from jdriftx.benchmarks.metriques import fac2, nmse
from jdriftx.experiences.evaluation_puff import SourceImpulsionnelle
from jdriftx.experiences.reference_independante import (
    DIFFUSION_BRIGGS,
    PARAMETRES_EDP_DEFAUT,
    ModeleDiffusion,
    ParametresEdp,
)
from jdriftx.experiences.transitoire_puff.routes import (
    MesureEdpPuff,
    MesureFermeePuff,
    RouteEdpPuff,
    RouteFermeePuff,
    StructureLongitudinale,
)


class PointComparaisonPuff(BaseModel):
    """Comparaison ponctuelle fermée/EDP transitoire en un point de mesure."""

    model_config = ConfigDict(frozen=True)

    x: float
    y: float
    z: float
    fermee: float
    edp: float
    ratio: float


class ComparaisonTransitoire(BaseModel):
    """Comparaison complète de la route EDP transitoire à la solution fermée.

    Attributs :
        source_puff : identification de la source comparée (masse, vent, classe).
        parametres : paramètres numériques de la grille EDP transverse.
        instants : instants de passage couverts par la solution (s).
        points : comparaisons ponctuelles, une par point de mesure.
        fac2 : fraction des points dans un facteur 2 (prédiction entre 0,5
            et 2 fois la référence ; métrique partagée).
        nmse : erreur quadratique normalisée (somme des carrés des écarts
            sur la somme des carrés de la référence ; métrique partagée).
        ecart_relatif_max : écart relatif maximal fermée/EDP (sans unité).
        ecart_masse_max : écart relatif maximal de masse aux instantanés.
        cout_ferme_s : coût de la route fermée, mesuré (s).
        cout_edp_s : coût de la route EDP, mesuré séparément (s).
    """

    model_config = ConfigDict(frozen=True)

    source_puff: str
    parametres: ParametresEdp
    instants: tuple[float, ...]
    points: tuple[PointComparaisonPuff, ...]
    fac2: float
    nmse: float
    ecart_relatif_max: float
    ecart_masse_max: float
    cout_ferme_s: float
    cout_edp_s: float

    def vers_dict(self) -> dict[str, object]:
        """Exporte la comparaison en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


class ManifesteTransitoire(BaseModel):
    """Manifeste de l'EDP transitoire du puff (suite de l'étape 6)."""

    model_config = ConfigDict(frozen=True)

    identifiant: str
    niveau_fidelite: str
    source: str
    heritage_documentaire: str
    reconstruction: str
    extension: str
    limites: tuple[str, ...]
    comparaison: ComparaisonTransitoire
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


def assembler_comparaison(
    source: SourceImpulsionnelle,
    fermee: MesureFermeePuff,
    edp: MesureEdpPuff,
    points: tuple[PointMesure, ...],
    parametres: ParametresEdp,
) -> ComparaisonTransitoire:
    """Assemble les mesures typées des deux routes en comparaison dirigée.

    Assemblage pur, sans résolution : les routes sont mesurées séparément
    (note 35) et cette fonction n'en connaît que les mesures ; les points
    sont appariés strictement (zip strict), les métriques FAC2 (fraction
    des points dans un facteur deux) et NMSE (erreur quadratique
    normalisée) sont celles du registre partagé
    (jdriftx.benchmarks.metriques, issue #43), et les coûts reportés sont
    exactement ceux des mesures.
    """
    comparaisons = tuple(
        PointComparaisonPuff(
            x=float(point.x),
            y=float(point.y),
            z=float(point.z),
            fermee=valeur_fermee,
            edp=valeur_edp,
            ratio=float(valeur_edp / valeur_fermee),
        )
        for point, valeur_fermee, valeur_edp in zip(
            points, fermee.valeurs, edp.valeurs, strict=True
        )
    )
    ecarts_relatifs = [abs(point.edp - point.fermee) / point.fermee for point in comparaisons]
    return ComparaisonTransitoire(
        source_puff=(
            f"masse={source.masse} kg, u={source.u} m/s, classe={source.classe}, x0={source.x0} m"
        ),
        parametres=parametres,
        instants=tuple(float(instant.t) for instant in edp.solution.instants),
        points=comparaisons,
        fac2=fac2(list(fermee.valeurs), list(edp.valeurs)),
        nmse=nmse(list(fermee.valeurs), list(edp.valeurs)),
        ecart_relatif_max=float(max(ecarts_relatifs)),
        ecart_masse_max=float(max(edp.ecarts_masse)),
        cout_ferme_s=fermee.cout_s,
        cout_edp_s=edp.cout_s,
    )


def comparer_transitoire(
    source: SourceImpulsionnelle,
    arcs: tuple[float, ...],
    points: tuple[PointMesure, ...],
    parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
    modele: ModeleDiffusion = DIFFUSION_BRIGGS,
    structure: StructureLongitudinale | None = None,
) -> ComparaisonTransitoire:
    """Compare la route EDP transitoire à la solution fermée aux passages.

    Orchestration seulement : la route fermée évalue la solution fermée du
    puff aux instants de passage, la route EDP résout la marginale
    transverse puis lui applique la structure longitudinale injectée, et
    l'assemblage des mesures typées en métriques est délégué à
    ``assembler_comparaison`` ; les coûts des deux routes sont mesurés
    séparément (note 35), sans facteur historique.
    """
    fermee = RouteFermeePuff(source, arcs).mesurer(points)
    mesure = RouteEdpPuff(source, arcs, parametres, modele, structure).mesurer(points)
    return assembler_comparaison(source, fermee, mesure, points, parametres)


def construire_manifeste(comparaison: ComparaisonTransitoire) -> ManifesteTransitoire:
    """Construit le manifeste étiqueté de l'EDP transitoire (statuts figés).

    Le manifeste porte l'étiquetage héritage/reconstruction/extension et
    les limites explicites ; la version du code est lue dans les
    métadonnées d'installation si disponible, « non-installe » sinon.
    """
    try:
        version = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version = "non-installe"
    return ManifesteTransitoire(
        identifiant="jdriftx-transitoire-puff-001",
        niveau_fidelite="R1",
        source="Chapitre « Reduced-Order Modelling of Dispersion » (Brun & "
        "Mohammadi, 2008), DOI 10.1007/978-1-4020-8758-5_14",
        heritage_documentaire=(
            "Aucune source historique : l'EDP transitoire du puff est la "
            "suite directe de l'évaluation dirigée du puff (note 53) ; aucun "
            "chiffre de l'ouvrage de 2008 n'est utilisé comme cible."
        ),
        reconstruction=(
            "Marche explicite FTCS en temps de la marginale transverse du puff "
            "(nombre de Fourier ≤ 1/3 au dernier passage, entrée fermée au "
            "premier instant de passage, miroir au sol, Dirichlet aux bords) ; "
            "structure longitudinale analytique (carte travel-time de la note "
            "37, isotropie sigma_x = sigma_y du noyau fermé)."
        ),
        extension=(
            "EDP transitoire du puff : seconde extension conditionnelle du "
            "contrat minimal (docs/47 §5) ; la source impulsionnelle de la "
            "note 53 reçoit sa route EDP transitoire, hors périmètre de la "
            "baseline continue."
        ),
        limites=(
            "Contrôle d'auto-cohérence entre deux routes du même package sur "
            "un cas synthétique : pas une validation physique.",
            "La structure longitudinale reste analytique (carte travel-time, "
            "isotropie du noyau fermé) : seule la marginale transverse est "
            "marchée numériquement.",
            "Le noyau du puff est symétrique en z autour du sol : la moitié "
            "de la masse du noyau fermé est formellement sous le sol ; la "
            "grille porte la demi-colonne miroir et les écarts de masse sont "
            "comparés à la marginale analytique sur la même grille.",
            "Fenêtre tronquée à quatre écarts-types au dernier passage, "
            "grille calibrée pour la classe C du cas S0 figé (docs/48 §2.2).",
        ),
        comparaison=comparaison,
        version_code=version,
        commande=(
            "uv run python -c 'from jdriftx.benchmarks.cas import "
            "CAS_S0_DEFAUT; from jdriftx.experiences.evaluation_puff import "
            "PUFF_DEFAUT; from jdriftx.experiences.transitoire_puff import "
            "comparer_transitoire, construire_manifeste; "
            "print(construire_manifeste(comparer_transitoire(PUFF_DEFAUT, "
            "CAS_S0_DEFAUT.arcs, CAS_S0_DEFAUT.points())))'"
        ),
    )
