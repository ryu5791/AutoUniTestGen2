#include "func_003.h"

/**
 * func_003 - 2つのif文を持つMC/DC対象関数
 *
 * IF1: (a >= 10 && b < 5)  → return 1
 * IF2: (b >= 5 || c == 0)  → return 2
 * default                   → return 0
 */
int func_003(int a, int b, int c) {
    if (a >= 10 && b < 5) {
        return 1;
    }
    if (b >= 5 || c == 0) {
        return 2;
    }
    return 0;
}
