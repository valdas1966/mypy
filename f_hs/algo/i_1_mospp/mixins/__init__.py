from f_core.imports import ULazy

ULazy.install(globals(), {
    'ExtendableMOSPP': 'f_hs.algo.i_1_mospp.mixins.extendable:ExtendableMOSPP',
    'is_extendable': 'f_hs.algo.i_1_mospp.mixins.extendable:is_extendable',
})
