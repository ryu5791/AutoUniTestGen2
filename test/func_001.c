#include "func_001.h"

/**
 * func_001 - 2条件のAND演算によるMC/DC対象関数
 *
 * if文: (a > 0) && (b > 0)
 * 条件A: a > 0
 * 条件B: b > 0
 */
int func_001(int a, int b) {
    if (a > 0 && b > 0) {
        return 1;
    }
    return 0;
}
