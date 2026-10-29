"""Squelette de benchmarks : cas synthetiques, metriques et evaluation.

Trois modules isoles pour evoluer separement (docs/39) : cas (contrat
CasSynthetique et registre des cas), metriques (registre pre-enregistre
FAC2/NMSE) et reference (pipeline d evaluation et commande). Garde-fou
: le cas S0 n est pas une validation physique ; porte G1 (issue #204)
avant tout benchmark applicatif.
"""

from jdriftx.benchmarks.cas import (
    CAS_S0_DEFAUT,
    CasS0,
    CasSynthetique,
    PointMesure,
    construire_cas,
    enregistrer_cas,
    lister_cas,
    retirer_cas,
)
from jdriftx.benchmarks.metriques import (
    FAC2,
    METRIQUES,
    METRIQUES_DEFAUT,
    NMSE,
    Metrique,
    calculer_metriques,
    enregistrer_metrique,
    fac2,
    nmse,
    retirer_metrique,
)
from jdriftx.benchmarks.reference import (
    ResultatEvaluation,
    evaluer_prediction,
    main,
    mesurer_cout_inference,
)

__all__ = [
    "CAS_S0_DEFAUT",
    "FAC2",
    "METRIQUES",
    "METRIQUES_DEFAUT",
    "NMSE",
    "CasS0",
    "CasSynthetique",
    "Metrique",
    "PointMesure",
    "ResultatEvaluation",
    "calculer_metriques",
    "construire_cas",
    "enregistrer_cas",
    "enregistrer_metrique",
    "evaluer_prediction",
    "fac2",
    "lister_cas",
    "main",
    "mesurer_cout_inference",
    "nmse",
    "retirer_cas",
    "retirer_metrique",
]
