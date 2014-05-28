
#
# Copyright (C) 2011 The Guava Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
#

#
# MurmurHash3 was written by Austin Appleby, and is placed in the public
# domain. The author hereby disclaims copyright to this source code.
#

#
# Source:
# http://code.google.com/p/smhasher/source/browse/trunk/MurmurHash3.cpp
# (Modified to adapt to Guava coding conventions and to use the HashFunction interface)
#

#
# Modified to remove stuff Clojure doesn't need, placed under clojure.lang namespace,
# all fns made static, added hashOrdered/Unordered
#

# Ported to RPython by Timothy Baldridge


seed = 0
C1 = 0xcc9e2d51
C2 = 0x1b873593

def hash_int(input):
    if input == 0:
        return 0
    k1 = mixK1(input)
    h1 = mixH1(seed, k1)

    return fmix(h1, 4)

CHAR_BIT = 8

def rotl(value, shift):
    return (value << shift) | (value >> (32 - shift))

def rotr(value, shift):
    return (value >> shift) | (value << (32 - shift))

def mix_col_hash(hash, count):
    h1 = seed
    k1 = mixK1(hash)
    h1 = mixH1(h1, k1)
    return fmix(h1, count)

def mixK1(k1):
    k1 *= C1
    k1 = rotl(k1, 13)
    k1 *= C2
    return k1

def mixH1(h1, k1):
    h1 ^= k1
    h1 = rotl(h1, 13)
    h1 = h1 * 5 + 0xe6546b64
    return h1

def fmix(h1, length):
    h1 ^= length
    h1 ^= h1 >> 16
    h1 *= 0x85ebca6b
    h1 ^= h1 >> 13
    h1 *= 0xc2b2ae35
    h1 ^= h1 >> 16
    return h1