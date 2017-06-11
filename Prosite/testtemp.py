#!/usr/bin/python

import tempfile as tf

hello = tf.NamedTemporaryFile()

hello.write("hello\n")
hello.seek(0)

print hello.read().strip()
