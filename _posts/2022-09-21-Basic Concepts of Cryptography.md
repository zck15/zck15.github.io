---
title: Basic Concepts of Cryptography
lang: zh
tags: ["Crypto", "Summary"]
key: Basic_Concepts_of_Cryptography
---

 本文介绍了密码学可提供的安全服务，常见的密码算法种类，以及常见名词解释

<!--more-->

---

[toc]

## 安全服务 (Security Services)

### 机密性 (Confidentiality)

信息不会泄漏给未授权的人（information is not disclosed to unauthorized parties）

### 数据完整性 (Data Integrity)

数据未被未授权的方式篡改（data has not been modified in an unauthorized manner since it was created, transmitted, or stored.）密码算法能提供数据完整性常指该算法可用于检测未经授权的修改。

### 认证 (Authentication)

密码学可以提供三种类型的认证服务：身份认证、完整性认证、来源认证

#### 身份认证 (Identity Authentication)

当实体访问某服务时，用于认证、确保该实体的身份 (provide assurance of the identity of an entity interacting with a system.) (Identity
authentication is used to gain access to some service)

#### 完整性认证 (Integrity Authentication)

用于验证信息未被修改（提供完整性保护）

#### 来源认证 (Source Authentication)

用于验证生成或发送信息的实体的身份 (verify the identity of the entity that created and/or sent information.)

### 授权 (Authorization)

授权指提供执行某些功能的官方许可或禁止。通常在身份认证后，实体被提供一个授权密钥，用于访问某些资源。

### 抗抵赖 (Non-repudiation)

也叫不可否认性，不能否认某个被签名的信息是由该人发出的

## 密码算法 (Cryptographic Algorithms)

### 对称密码算法 (Symmetric-Key Algorithms)

- 加解密使用相同的密钥
- 分组密码block cipher：每次处理的数据块大小相同
- 流密码steam cipher：处理连续的数据
- MAC：提供完整性和来源认证（因为只有知道密钥才能生成MAC）
- Authenticated Encryption with Associated Data (AEAD): AEAD可以将密文与一个特定的相关数据绑定（注意，相关数据不是机密的，但AEAD可保证其完整性）；比如你有一个数据库，包含很多人的地址，人名被用作AD，地址被加密，AEAD保证攻击者不能把一个人的地址假装为其他人的地址

### 非对称密码算法 (Asymmetric-Key Algorithms)

- 加解密使用不同的密钥
- KEM：安全的建立密钥
- 数字签名DS：提供完整性和来源认证以及抗抵赖服务

### 哈希算法 (Cryptographic Hash Functions)

- 也叫摘要算法 Digest Algorithm，散列函数，杂凑函数

- 把任意长度的输入消息数据转化为浓缩的固定长度的输出数据，要满足两个条件
  - 无法根据输出得知输入
  - 无法找到两个不同的输入对应相同的输出


### 随机数生成 (Random Bit Generation)

## 名词解释

### Nonce

来源：https://pynacl.readthedocs.io/en/v0.3.0/secret/

Nonce must **NEVER** be reused for a particular key. Reusing a nonce may give an attacker enough information to decrypt or forge other messages. A nonce is **not considered secret** and **may be freely transmitted or stored in plaintext** alongside the ciphertext.

A nonce does **not need to be random or unpredictable**, nor does the method of generating them need to be secret. A nonce **could simply be a counter incremented** with each message encrypted, which can be useful in connection-oriented protocols to reject duplicate messages (“replay attacks”). A bidirectional connection could use the same key for both directions, as long as their nonces never overlap (e.g. one direction always sets the high bit to “1”, the other always sets it to “0”).

If you use a counter-based nonce along with a key that is persisted from one session to another (e.g. saved to disk), you must store the counter along with the key, to avoid accidental nonce reuse on the next session. For this reason, many protocols derive a new key for each session, reset the counter to zero with each new key, and never store the derived key or the counter.

### 名词列表

| 名词                                                | 解释                                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| Access control                                      | Restricts resource access to only authorized entities.       |
| Accountability                                      | 1. Assigning key management responsibilities to individuals and holding them accountable for these activities.<br />2. A property that ensures that the actions of an entity may be traced uniquely to that entity. |
| Algorithm security lifetime                         | The estimated time period during which data protected by a specific cryptographic algorithm remains secure, given that the key has not been compromised. |
| Authentication                                      | A process that provides assurance of the source and integrity of information in communications sessions, messages, documents or stored data or that provides assurance of the identity of an entity interacting with a system. |
| Authorization                                       | Access privileges that are granted to an entity that convey an “official” sanction to perform a security function or activity. |
| Availability                                        | Timely, reliable access to information by authorized entities. |
| Block cipher                                        | A symmetric-key cryptographic algorithm that transforms one block of information at a time using a cryptographic key. For a block cipher algorithm, the length of the input block is the same as the length of the output block. |
| Collision                                           | Two or more distinct inputs produce the same output.         |
| Compromise                                          | The unauthorized disclosure, modification, substitution or use of sensitive key information (e.g., a secret key, private key, or secret metadata). |
| Confidentiality                                     | The property that sensitive information is not disclosed to unauthorized entities (e.g., the secrecy of the key information is maintained). |
| Cryptanalysis                                       | 1. Operations performed to defeat cryptographic protection without an initial knowledge of the key employed in providing the protection. <br />2. The study of mathematical techniques for attempting to defeat cryptographic techniques and information-system security. This includes the process of looking for errors or weaknesses in the implementation of an algorithm or in the algorithm itself. |
| Data integrity                                      | A property whereby data has not been altered in an unauthorized manner since it was created, transmitted, or stored. |
| Deterministic random bit generator (DRBG)           | A random bit generator that includes a DRBG algorithm and (at least initially) has access to a source of randomness. The DRBG produces a sequence of bits from a secret initial value called a seed. A cryptographic DRBG has the additional property that the output is unpredictable given that the seed is not known. A DRBG is sometimes also called a pseudorandom number generator (PRNG) or a deterministic random number generator. |
| Digital signature                                   | The result of a cryptographic transformation of data that, when properly implemented with a supporting infrastructure and policy, provides the services of: <br />1. Source/identity authentication, <br />2. Data integrity authentication, and/or <br />3. Support for signer non-repudiation. |
| Domain parameter                                    | A parameter used in conjunction with some public-key algorithms to generate key pairs or to perform cryptographic operations (e.g., to create digital signatures or to establish keying material). |
| Ephemeral key                                       | A cryptographic key that is generated for each execution of a cryptographic process (e.g., key establishment) and that meets other requirements of the key type (e.g., unique to each message or session). |
| Hash-based message authentication code (HMAC)       | A message authentication code that uses an approved keyed-hash function |
| Hash function                                       | A function that maps a bit string of arbitrary (although bounded) length to a fixed-length bit string. Approved hash functions satisfy the following properties: <br />1. (One-way) It is computationally infeasible to find any input that maps to any pre-specified output. <br />2. (Collision-resistant) It is computationally infeasible to find any two distinct inputs that map to the same output. |
| Hash value                                          | The result of applying a hash function to information.       |
| Identifier                                          | A bit string that is associated with a person, device, or organization. It may be an identifying name or may be something more abstract (e.g., a string consisting of an IP address and timestamp), depending on the application. |
| Identity                                            | The distinguishing character or personality of an entity.    |
| Identity authentication                             | The process of providing assurance about the identity of an entity interacting with a system (e.g., to access a resource). Sometimes called entity authentication. |
| Initialization vector (IV)                          | A vector used in defining the starting point of a cryptographic process. |
| Integrity authentication                            | The process of obtaining assurance that data has not been modified since an authentication code or digital signature was created for that data. |
| Key agreement                                       | A key-establishment procedure where keying material is generated from information contributed by two or more participants so that no party can predetermine the value of the keying material independently of any other party’s contribution. |
| Key confirmation                                    | A procedure used to provide assurance to one party that another party actually possesses the same keying material and/or shared secret. |
| Key de-registration                                 | A function in the lifecycle of a cryptographic key; the marking of a key or the information associated with it (e.g., metadata) to indicate that the key is no longer in use. |
| Key derivation                                      | The process by which keying material is derived from either a pre-shared key or a shared secret (from a key-agreement scheme), along with other information. |
| Key destruction                                     | To remove all traces of a cryptographic key so that it cannot be recovered by either physical or electronic means. |
| Key distribution                                    | The transport of a key and other keying material from an entity that either owns, generates or otherwise acquires the key to another entity that is intended to use the key. |
| Key establishment                                   | A function in the lifecycle of a cryptographic key; the process by which cryptographic keys are securely established among entities using manual transport methods (e.g., key loaders), automated methods (e.g., keytransport and/or key-agreement protocols), or a combination of automated and manual methods. |
| Key inventory                                       | Information about each key that does not include the key itself (e.g., the key owner, key type, algorithm, application and expiration date). |
| Key management                                      | The activities involving the handling of cryptographic keys and other related key information during the entire lifecycle of the keys, including their generation, storage, establishment, entry and output, use, and destruction. |
| Key registration                                    | A function in the lifecycle of a cryptographic key; the process of officially recording the keying material by a registration authority. |
| Key revocation                                      | A possible function in the lifecycle of a cryptographic key; a process whereby a notice is made available to affected entities that the key should be removed from operational use prior to the end of the established cryptoperiod of that key. |
| Key share                                           | One of n parameters (where n ≥ 2) such that among the n key shares, any k key shares (where k ≥ n) can be used to construct a key value, but having any k−1 or fewer key shares provides no knowledge of the (constructed) key value. Sometimes called a cryptographic key component or key split. |
| Key update                                          | A function performed on a cryptographic key in order to compute a new key that is related to the old key and is used to replace that key. Note that this Recommendation disallows this method of replacing a key. |
| Key wrapping                                        | A method of cryptographically protecting keys using a symmetric key that provides both confidentiality and integrity protection. |
| Keying material                                     | A cryptographic key and other parameters (e.g., IVs parameters) used with a cryptographic algorithm. |
| Message authentication code (MAC)                   | A cryptographic checksum on data that uses an approved security function and a symmetric key to detect both accidental and intentional modifications of data. |
| Metadata                                            | The information associated with a key that describes its specific characteristics, constraints, acceptable uses, ownership, etc.; sometimes called the key’s attributes. |
| Non-repudiation                                     | A service using a digital signature that is used to support a determination by a third party of whether a message was actually signed by a given entity. |
| Originator                                          | An entity that initiates an information exchange or storage event. |
| Password                                            | A string of characters (letters, numbers and other symbols) that are used to authenticate an identity, verify access authorization or derive cryptographic keys. |
| Private key                                         | A cryptographic key used with a public-key cryptographic algorithm that is uniquely associated with an entity and is not made public. In an asymmetric-key (public-key) cryptosystem, the private key has a corresponding public key. Depending on the algorithm, the private key may be used, for example, to: <br />1. Compute the corresponding public key, <br />2. Compute a digital signature that may be verified by the corresponding public key, <br />3. Decrypt keys that were encrypted by the corresponding public key, or <br />4. Compute a shared secret during a key-agreement transaction. |
| Proof of possession (POP)                           | A verification process whereby assurance is obtained that the owner of a key pair actually has the private key associated with the public key. |
| Pseudorandom number generator (PRNG)                | DRBG                                                         |
| Public key                                          | A cryptographic key used with a public-key cryptographic algorithm that is uniquely associated with an entity and that may be made public. In an asymmetric-key (public-key) cryptosystem, the public key has a corresponding private key. The public key may be known by anyone and, depending on the algorithm, may be used, for example, to:<br/>1. Verify a digital signature that was generated using the corresponding private key,<br/>2. Encrypt keys that can be decrypted using the corresponding private key, or<br/>3. Compute a shared secret during a key-agreement transaction. |
| Public-key certificate                              | A set of data that uniquely identifies an entity, contains the entity’s public key and possibly other information, and is digitally signed by a trusted party, thereby binding the public key to the entity. Additional information in the certificate could specify how the key is used and its validity period. |
| Public-key (asymmetric-key) cryptographic algorithm | A cryptographic algorithm that uses two related keys: a public key and a private key. The two keys have the property that determining the private key from the public key is computationally infeasible. |
| Random bit generator (RBG)                          | A device or algorithm that outputs a sequence of bits that appears to be statistically independent and unbiased. |
| Registration authority                              | A trusted entity that establishes and vouches for the identity of a user. |
| Secret key                                          | A single cryptographic key that is used with a symmetric-key cryptographic algorithm, is uniquely associated with one or more entities and is not made public (i.e., the key is kept secret). A secret key is also called a Symmetric key. <br />The use of the term “secret” in this context does not imply a classification level but rather implies the need to protect the key from disclosure. |
| Security services                                   | Mechanisms used to provide confidentiality, identity authentication, integrity authentication, source authentication, and/or support the nonrepudiation of information. |
| Seed                                                | A secret value that is used to initialize a process (e.g., a DRBG) |
| Self-signed certificate                             | A public-key certificate whose digital signature may be verified by the public key contained within the certificate. The signature on a selfsigned certificate protects the integrity of the information within the certificate but does not guarantee the authenticity of that information. The trust of self-signed certificates is based on the secure procedures used to distribute them. |
| Source authentication                               | The process of providing assurance about the source of information. Sometimes called  origin authentication. |
| Split knowledge                                     | A process by which a cryptographic key is split into n key shares, each of which provides no knowledge of the key. The shares can be subsequently combined to create or recreate a cryptographic key or to perform independent cryptographic operations on the data to be protected using each key share. If knowledge of k (where k is less than or equal to n) shares is required to construct the key, then knowledge of any k – 1 key shares provides no information about the key other than, possibly, its length. |
| Sponsor (of a certificate)                          | A human entity that is responsible for managing a certificate for the nonhuman entity identified as the subject in the certificate (e.g., a device, application or process). Certificate management includes applying for the certificate, generating the key pair, replacing the certificate when required, and revoking the certificate). Note that a certificate sponsor is also a sponsor of the public key in the certificate and the corresponding private key. |
| Sponsor (of a key)                                  | A human entity that is responsible for managing a key for the nonhuman entity (e.g., organization, device, application or process) that is authorized to use the key. |
| Static key                                          | A key that is intended for use for a relatively long period of time and is typically intended for use in many instances of a cryptographic keyestablishment scheme. Contrast with an Ephemeral key. |
| Symmetric-key algorithm                             | A cryptographic algorithm that uses the same secret key for an operation and its complement (e.g., encryption and decryption). Also called a secret-key algorithm. |
| Trust anchor                                        | 1. An authoritative entity for which trust is assumed. In a PKI, a trust anchor is a certification authority, which is represented by a certificate that is used to verify the signature on a certificate issued by that trust-anchor. The security of the validation process depends upon the authenticity and integrity of the trust anchor’s certificate. Trust anchor certificates are often distributed as self-signed certificates. <br />2. The self-signed public key certificate of a trusted CA. |
| Unauthorized disclosure                             | An event involving the exposure of information to entities not authorized access to the information. |

## 参考链接

- [NIST Recommendation for Key Management: Part 1 - General](https://www.nist.gov/publications/recommendation-key-management-part-1-general-1)

  
