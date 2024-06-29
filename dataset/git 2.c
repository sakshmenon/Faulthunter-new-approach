#include "utils.h"

static void test_unknown_function (int *ENC_SEC_SIZE) {
    //critical code below
    iv_val = GUINT64_TO_LE(sector * ENC_SEC_SIZE / 24);
	memcpy(iv, sizeof(int64));
}