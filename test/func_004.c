#include "func_004.h"

/**
 * func_004 - NOT演算子を含む2つのif文を持つMC/DC対象関数
 *
 * IF1: (a > 0 && b != 0)      → return 1
 * IF2: (!(a > 0) || c >= 10)  → return 2
 * default                      → return 0
 */
int func_004(int a, int b, int c) {
    if (a > 0 && b != 0) {
        return 1;
    }
    if (!(a > 0) || c >= 10) {
        return 2;
    }
    return 0;
}
