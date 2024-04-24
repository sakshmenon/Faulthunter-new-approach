#include "cryptlib.h"
static uint64_t rbuf_hash_cb(void *instance, void *env) {
    //critical code below
    rbuf *r = (rbuf *)instance;
    (void)env;
    return theft_hash_onepass(r->buf, r->size);
}