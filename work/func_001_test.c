#include "unity.h"
#include "func_001.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: a > 0 && b > 0 */
void test_func_001_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_001(1, 1));
}

/* IF1: a > 0 && b > 0 */
void test_func_001_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_001(1, 0));
}

/* IF1: a > 0 && b > 0 */
void test_func_001_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_001(0, 1));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_001_IF1_TC1);
    RUN_TEST(test_func_001_IF1_TC2);
    RUN_TEST(test_func_001_IF1_TC3);
    return UNITY_END();
}
