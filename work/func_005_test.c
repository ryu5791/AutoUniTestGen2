#include "unity.h"
#include "func_005.h"

void setUp(void) {}
void tearDown(void) {}

/* IF1: a > 0 && b > 0 */
void test_func_005_IF1_TC1(void) {
    TEST_ASSERT_EQUAL_INT(1, func_005(1, 1, 0, 0));
}

/* IF1: a > 0 && b > 0 */
void test_func_005_IF1_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_005(1, 0, 0, 0));
}

/* IF1: a > 0 && b > 0 */
void test_func_005_IF1_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_005(0, 1, 0, 0));
}

/* IF2: c > 5 || b < 0 */
void test_func_005_IF2_TC1(void) {
    TEST_ASSERT_EQUAL_INT(2, func_005(0, 0, 6, 0));
}

/* IF2: c > 5 || b < 0 */
void test_func_005_IF2_TC2(void) {
    TEST_ASSERT_EQUAL_INT(2, func_005(0, -1, 5, 0));
}

/* IF2: c > 5 || b < 0 */
void test_func_005_IF2_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_005(0, 0, 5, 0));
}

/* IF3: a <= 0 && d >= 3 */
void test_func_005_IF3_TC1(void) {
    TEST_ASSERT_EQUAL_INT(3, func_005(0, 0, 0, 3));
}

/* IF3: a <= 0 && d >= 3 */
void test_func_005_IF3_TC2(void) {
    TEST_ASSERT_EQUAL_INT(0, func_005(0, 0, 0, 2));
}

/* IF3: a <= 0 && d >= 3 */
void test_func_005_IF3_TC3(void) {
    TEST_ASSERT_EQUAL_INT(0, func_005(1, 0, 0, 3));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_func_005_IF1_TC1);
    RUN_TEST(test_func_005_IF1_TC2);
    RUN_TEST(test_func_005_IF1_TC3);
    RUN_TEST(test_func_005_IF2_TC1);
    RUN_TEST(test_func_005_IF2_TC2);
    RUN_TEST(test_func_005_IF2_TC3);
    RUN_TEST(test_func_005_IF3_TC1);
    RUN_TEST(test_func_005_IF3_TC2);
    RUN_TEST(test_func_005_IF3_TC3);
    return UNITY_END();
}
