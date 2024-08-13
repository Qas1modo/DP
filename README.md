## Side-Channel Analysis Project: implementing and evalauting side-channel security of Java cryptographic implementations running on JavaCard ##

Physical security threats appear at the chip level, where an attacker can measure or physically influence a cryptographic operation performed by the chip's circuit.
The side-channel analysis exploits additional sources of information (called physical observations), including timing, power consumption, or electromagnetic emissions (EM), among others.
Malicious data modifications can be caused by fault injection, which can be performed using optical, electromagnetic, power, and clock glitches.
These attacks pose a serious threat to modern cryptographic implementations. The goal of the project is to implement and evaluate the security of modern cryptography implemented in Java for JavaCard. 
As an example of modern cryptography, we will consider Ascon and another scheme chosen by the student (for example, AES or a lightweight cryptographic scheme). 
I am open to considering another cryptographic scheme if the student is interested). The project will start with taking a JavaCard implementation of ASCON and the other scheme and evaluating their security. 
Subsequently, the student will have a look at side-channel protections; alternatively, if a student is more interested in protections, then this can be a more significant part of the thesis, and the other
scheme can be skipped.

Run Main with python 3.10
