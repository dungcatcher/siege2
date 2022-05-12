import colorsys


def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t


def rgb_to_hsv(rgb):
    norm_r, norm_g, norm_b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    return colorsys.rgb_to_hsv(norm_r, norm_g, norm_b)


def hsv_to_rgb(hsv):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))


def colour_interpolate(colour1, colour2, t):
    hsv1 = rgb_to_hsv(colour1)
    hsv2 = rgb_to_hsv(colour2)

    final_hsv_h = lerp(hsv1[0], hsv2[0], t)
    final_hsv_s = lerp(hsv1[1], hsv2[1], t)
    final_hsv_v = lerp(hsv1[2], hsv2[2], t)
    final_hsv = (final_hsv_h, final_hsv_s, final_hsv_v)
    return hsv_to_rgb(final_hsv)



