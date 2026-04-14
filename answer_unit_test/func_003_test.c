#include "unity.h"
#include "func_003.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: a >= 10 && b < 5 */
void test_func_003_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_003(10, 4, 1));
}

/* IF1: a >= 10 && b < 5 */
void test_func_003_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_003(9, 4, 1));
}

/* IF1: a >= 10 && b < 5 */
void test_func_003_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(2, func_003(10, 5, 1));
}

/* IF2: b >= 5 || c == 0 */
void test_func_003_IF2_TC4(void) {
    TEST_ASSERT_EQUAL_INT(2, func_003(9, 5, 1));
}

/* IF2: b >= 5 || c == 0 */
void test_func_003_IF2_TC5(void) {
    TEST_ASSERT_EQUAL_INT(2, func_003(9, 4, 0));
}

/* IF2: b >= 5 || c == 0 */
void test_func_003_IF2_TC6(void) {
    TEST_ASSERT_EQUAL_INT(0, func_003(9, 4, 1));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_003_IF1_TC1);
    RUN_TEST(test_func_003_IF1_TC2);
    RUN_TEST(test_func_003_IF1_TC3);
    RUN_TEST(test_func_003_IF2_TC4);
    RUN_TEST(test_func_003_IF2_TC5);
    RUN_TEST(test_func_003_IF2_TC6);
    return UNITY_END();
}
