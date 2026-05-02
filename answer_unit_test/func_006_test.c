#include "unity.h"
#include "func_006.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: a > 0 && b >= 3 && c != 0 */
void test_func_006_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_006(1, 3, 1, 0));
}

/* IF1: a > 0 && b >= 3 && c != 0 */
void test_func_006_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_006(1, 3, 0, 0));
}

/* IF1: a > 0 && b >= 3 && c != 0 */
void test_func_006_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_006(1, 2, 1, 0));
}

/* IF1: a > 0 && b >= 3 && c != 0 */
void test_func_006_IF1_TC4(void) {
    TEST_ASSERT_EQUAL_INT(0, func_006(0, 3, 1, 0));
}

/* IF2: b < 0 || d > 10 */
void test_func_006_IF2_TC1(void) {
    TEST_ASSERT_EQUAL_INT(2, func_006(0, -1, 0, 10));
}

/* IF2: b < 0 || d > 10 */
void test_func_006_IF2_TC2(void) {
    TEST_ASSERT_EQUAL_INT(2, func_006(0, 0, 0, 11));
}

/* IF2: b < 0 || d > 10 */
void test_func_006_IF2_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_006(0, 0, 0, 10));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_006_IF1_TC1);
    RUN_TEST(test_func_006_IF1_TC2);
    RUN_TEST(test_func_006_IF1_TC3);
    RUN_TEST(test_func_006_IF1_TC4);
    RUN_TEST(test_func_006_IF2_TC1);
    RUN_TEST(test_func_006_IF2_TC2);
    RUN_TEST(test_func_006_IF2_TC3);
    return UNITY_END();
}
