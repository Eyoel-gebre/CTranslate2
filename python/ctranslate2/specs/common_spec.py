import enum

from ctranslate2.specs import model_spec


# This enum should match the C++ equivalent in include/ctranslate2/ops/activation.h.
class Activation(enum.IntEnum):
    """Activation type."""

    RELU = 0
    GELUTanh = 1
    SWISH = 2
    GELU = 3
    GELUSigmoid = 4
    Tanh = 5
    Sigmoid = 6


# This enum should match the C++ equivalent in include/ctranslate2/layers/common.h.
class EmbeddingsMerge(enum.IntEnum):
    """Merge strategy for factors embeddings."""

    CONCAT = 0
    ADD = 1


class Quantization(enum.IntEnum):
    """Activation type."""

    CT2 = 0
    AWQ_GEMM = 1
    AWQ_GEMV = 2


class LayerNormSpec(model_spec.LayerSpec):
    def __init__(self, rms_norm=False):
        self.gamma = None
        if not rms_norm:
            self.beta = None
        else:
            self.layer_norm_use_residual = model_spec.OPTIONAL


class LinearSpec(model_spec.LayerSpec):
    def __init__(self):
        self.weight = None
        self.weight_scale = model_spec.OPTIONAL
        self.weight_zero = model_spec.OPTIONAL
        self.bias = model_spec.OPTIONAL

    def has_bias(self):
        return not isinstance(self.bias, str)

class LowRankLinearSpec(model_spec.LayerSpec):
    def __init__(self):
        super().__init__()
        self.low_rank_weight_1 = None
        self.low_rank_weight_2 = None
        self.weight_scale = model_spec.OPTIONAL
        self.weight_zero = model_spec.OPTIONAL
        self.bias = model_spec.OPTIONAL

    def has_bias(self):
        return not isinstance(self.bias, str)


class Conv1DSpec(model_spec.LayerSpec):
    def __init__(self):
        self.weight = None
        self.weight_scale = model_spec.OPTIONAL
        self.bias = model_spec.OPTIONAL


class EmbeddingsSpec(model_spec.LayerSpec):
    def __init__(self):
        self.weight = None
        self.weight_scale = model_spec.OPTIONAL
        self.multiply_by_sqrt_depth = model_spec.OPTIONAL
