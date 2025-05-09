import enum

import numpy as np

from ctranslate2.specs import common_spec, model_spec


# This enum should match the C++ equivalent in include/ctranslate2/layers/attention.h.
class RotaryScalingType(enum.IntEnum):
    """RoPE scaling type."""

    Linear = 0
    Su = 1
    Llama3 = 2


class MultiHeadAttentionSpec(model_spec.LayerSpec):
    def __init__(
        self,
        self_attention=False,
        relative_position=False,
        relative_asymmetric_position=False,
        relative_attention_bias=False,
        rms_norm=False,
        rotary_dim=None,
        rotary_interleave=True,
        rotary_scaling_type=None,
        rotary_scaling_factor=1,
        rotary_base=10000,
        original_max_position_embeddings=0,
        max_position_embeddings=0,
        num_heads_kv=None,
        head_dim=None,
        sliding_window=None,
        low_rank=False,
    ):
        self.queries_scale = model_spec.OPTIONAL

        self.layer_norm = common_spec.LayerNormSpec(rms_norm=rms_norm)
        if low_rank:
            self.linear = [common_spec.LowRankLinearSpec() for _ in range(4)]
        else:
            self.linear = [
                common_spec.LinearSpec() for _ in range(2 if self_attention else 3)
            ]

        if relative_position:
            self.relative_position_keys = None
            self.relative_position_values = None

        if relative_attention_bias:
            self.relative_attention_bias = None
            self.relative_attention_max_distance = None

        if relative_asymmetric_position:
            self.relative_asymmetric_position_keys = None
            self.relative_left_max_position = None
            self.relative_right_max_position = None

        if original_max_position_embeddings != 0:
            self.original_max_position_embeddings = np.dtype("int32").type(
                original_max_position_embeddings
            )
        if max_position_embeddings != 0:
            self.max_position_embeddings = np.dtype("int32").type(
                max_position_embeddings
            )

        if rotary_dim is not None:
            self.rotary_dim = np.dtype("int32").type(rotary_dim)
            self.rotary_interleave = rotary_interleave
            self.rotary_base = np.dtype("float32").type(rotary_base)

            if rotary_scaling_type is not None:
                self.rotary_scaling_type = np.dtype("int8").type(rotary_scaling_type)
            if rotary_scaling_type is RotaryScalingType.Linear:
                self.rotary_scaling_factor = np.dtype("float32").type(
                    rotary_scaling_factor
                )
            elif rotary_scaling_type is RotaryScalingType.Su:
                self.rotary_scaling_long_factor = None
                self.rotary_scaling_short_factor = None
            elif rotary_scaling_type is RotaryScalingType.Llama3:
                self.rotary_low_freq_factor = None
                self.rotary_high_freq_factor = None

        if num_heads_kv is not None:
            self.num_heads_kv = np.dtype("int32").type(num_heads_kv)

        if head_dim is not None:
            self.head_dim = np.dtype("int32").type(head_dim)

        if sliding_window is not None:
            self.sliding_window = np.dtype("int32").type(sliding_window)
