#include "func_005.h"

/**
 * func_005 - 3つのif文を持つMC/DC対象関数（最高複雑度）
 *
 * IF1: (a > 0 && b > 0)         → return 1
 * IF2: (c > 5 || b < 0)         → return 2
 * IF3: (a <= 0 && d >= 3)       → return 3
 * default                        → return 0
 *
 * IF3到達条件: IF1=F(a<=0 or b<=0) AND IF2=F(c<=5 and b>=0)
 * → a<=0, b=0, c<=5 でIF3に到達可能
 */
int func_005(int a, int b, int c, int d) {
    if (a > 0 && b > 0) {
        return 1;
    }
    if (c > 5 || b < 0) {
        return 2;
    }
    if (a <= 0 && d >= 3) {
        return 3;
    }
    return 0;
}
