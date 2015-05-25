#include "os_gl.h"
#ifdef __cplusplus
extern "C" {
#endif
#if defined(PURE_OPENGL_ES_2)
#elif defined(OPENGL_ES_2)
/* these are the shaders that uses ES2 */
extern const char* default_vs;
extern const char* default_fs;
#else
/* these are the original default shaders */
extern const char* default_vs;
extern const char* default_fs;
#endif
extern const char* volume_vs;
extern const char* volume_fs;
extern const char* sphere_vs;
extern const char* sphere_fs;
extern const char* spheredirect_vs;
extern const char* cylinder_vs;
extern const char* cylinder_fs;
extern const char* sphere_arb_vs;
extern const char* sphere_arb_fs;
extern const char* indicator_vs;
extern const char* indicator_fs;
extern const char* compute_color_for_light_fs;
extern const char* call_compute_color_for_light_fs;
extern const char* compute_fog_color_fs;
extern const char* bg_vs;
extern const char* bg_fs;
extern const char* label_vs;
extern const char* label_fs;
extern const char* screen_vs;
extern const char* screen_fs;
extern const char* labelscreen_vs;
extern const char* labelscreen_fs;
extern const char* defaultscreen_vs;
extern const char* defaultscreen_fs;
extern const char* anaglyph_fs;
extern const char* anaglyph_header_fs;
extern const char* ramp_vs;
extern const char* ramp_fs;
#ifdef __cplusplus
}
#endif
