#include "unity.h"
#include "func_002.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: (a > 0 && b > 0) || (c > 5) */
void test_func_002_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_002(1, 1, 5));
}

/* IF1: (a > 0 && b > 0) || (c > 5) */
void test_func_002_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_002(0, 1, 5));
}

/* IF1: (a > 0 && b > 0) || (c > 5) */
void test_func_002_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_002(1, 0, 5));
}

/* IF1: (a > 0 && b > 0) || (c > 5) */
void test_func_002_IF1_TC4(void) {
    TEST_ASSERT_EQUAL_INT(1, func_002(1, 0, 6));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_002_IF1_TC1);
    RUN_TEST(test_func_002_IF1_TC2);
    RUN_TEST(test_func_002_IF1_TC3);
    RUN_TEST(test_func_002_IF1_TC4);
    return UNITY_END();
}
