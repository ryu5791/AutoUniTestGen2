#include "unity.h"
#include "func_004.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: a > 0 && b != 0 */
void test_func_004_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_004(1, 1, 1));
}

/* IF1: a > 0 && b != 0 */
void test_func_004_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(2, func_004(0, 1, 1));
}

/* IF1: a > 0 && b != 0 */
void test_func_004_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_004(1, 0, 1));
}

/* IF2: !(a > 0) || c >= 10 */
void test_func_004_IF2_TC4(void) {
    TEST_ASSERT_EQUAL_INT(2, func_004(0, 0, 1));
}

/* IF2: !(a > 0) || c >= 10 */
void test_func_004_IF2_TC5(void) {
    TEST_ASSERT_EQUAL_INT(2, func_004(1, 0, 10));
}

/* IF2: !(a > 0) || c >= 10 */
void test_func_004_IF2_TC6(void) {
    TEST_ASSERT_EQUAL_INT(0, func_004(1, 0, 1));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_004_IF1_TC1);
    RUN_TEST(test_func_004_IF1_TC2);
    RUN_TEST(test_func_004_IF1_TC3);
    RUN_TEST(test_func_004_IF2_TC4);
    RUN_TEST(test_func_004_IF2_TC5);
    RUN_TEST(test_func_004_IF2_TC6);
    return UNITY_END();
}
