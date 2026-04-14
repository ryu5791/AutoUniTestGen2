#include "func_002.h"

/**
 * func_002 - 3条件の混合論理演算によるMC/DC対象関数
 *
 * if文: (a > 0 && b > 0) || (c > 5)
 * 条件A: a > 0
 * 条件B: b > 0
 * 条件C: c > 5
 */
int func_002(int a, int b, int c) {
    if ((a > 0 && b > 0) || (c > 5)) {
        return 1;
    }
    return 0;
}
