#include "func_006.h"

/**
 * func_006 - 3条件&&と2条件||を持つMC/DC対象関数
 *
 * IF1: (a > 0 && b >= 3 && c != 0)  → return 1  (3アトミック条件)
 * IF2: (b < 0 || d > 10)             → return 2  (2アトミック条件)
 * default                             → return 0
 *
 * IF2到達条件: IF1=F → a<=0 or b<3 or c==0
 * IF2テスト: a=0とすることでIF1=F(a>0失敗)、IF2の各条件を独立変化可能
 */
int func_006(int a, int b, int c, int d) {
    if (a > 0 && b >= 3 && c != 0) {
        return 1;
    }
    if (b < 0 || d > 10) {
        return 2;
    }
    return 0;
}
