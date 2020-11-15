// ==============================================================
// Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2020.1 (64-bit)
// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// ==============================================================
#ifndef __linux__

#include "xstatus.h"
#include "xparameters.h"
#include "xpool.h"

extern XPool_Config XPool_ConfigTable[];

XPool_Config *XPool_LookupConfig(u16 DeviceId) {
	XPool_Config *ConfigPtr = NULL;

	int Index;

	for (Index = 0; Index < XPAR_XPOOL_NUM_INSTANCES; Index++) {
		if (XPool_ConfigTable[Index].DeviceId == DeviceId) {
			ConfigPtr = &XPool_ConfigTable[Index];
			break;
		}
	}

	return ConfigPtr;
}

int XPool_Initialize(XPool *InstancePtr, u16 DeviceId) {
	XPool_Config *ConfigPtr;

	Xil_AssertNonvoid(InstancePtr != NULL);

	ConfigPtr = XPool_LookupConfig(DeviceId);
	if (ConfigPtr == NULL) {
		InstancePtr->IsReady = 0;
		return (XST_DEVICE_NOT_FOUND);
	}

	return XPool_CfgInitialize(InstancePtr, ConfigPtr);
}

#endif

