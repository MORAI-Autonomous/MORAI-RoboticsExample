#!/usr/bin/env python
# -*- Encoding: utf-8 -*-

# from lib.simulator_command import *
from lib.define import * 

class status_parser:
    def __init__(self):
        ##Platform
        self.dict_data_platform={
            "0x01" : "Launcher",
            "0x02" : "Simulator"
        }

        ##Launcher
        self.dict_data_launcher_stage={
            "0x01" : "로그인 전 상태",
            "0x02" : "로그인 후 상태"
        }

        #launcher_status(0x01)
        self.dict_data_launcher_status1={            
            "0x0001" : "대기상태"
        }

        #launcher_status(0x02)
        self.dict_data_launcher_status2={                      
            "0x0001" : "시뮬레이터 버전 선택 됨",
            "0x0002" : "시뮬레이터 버전 선택 안됨",
            "0x0003" : "시뮬레이터 설치 필요 상태",
            "0x0004" : "에셋번들 다운로드 중",
            "0x0005" : "시뮬레이터 다운로드 중",
            "0x0006" : "로그인 완료 상태",
            "0x0007" : "시뮬레이터 종료 후 런쳐 대기상태"
        }
        
        ##Simulator
        self.dict_data_simulator_stage={            
            "0x01" : "로비 진입 상태",
            "0x02" : "플레이 상태"
        }        

        #simulator_status(0x01)
        self.dict_data_simulator_status1={            
            "0x0001" : "대기상태",
            "0x0002" : "맵/차량 선택 안됨",
            "0x0003" : "로딩중"
        }

        #simulator_status(0x02)
        self.dict_data_simulator_status2={                        
            "0x0001" : "대기 상태(플레이 상태)",
            "0x0002" : "시뮬레이션 정지 상태",
            "0x0003" : "로딩중",            
            "0x0004" : "종료 명령으로 인한 시뮬레이션 종료 중",
            "0x0005" : "맵 변경이 완료"
        }
        
        ##Result
        self.dict_result={
            "0x00" : "명령 없음",
            "0x01" : "성공",
            "0x11" : "유효하지 않은 플랫폼",
            "0x12" : "유효하지 않은 스테이지",
            "0x23" : "ID 오류",
            "0x24" : "PW 오류",
            "0x25" : "시뮬레이터 버전 오류",
            "0x26" : "시뮬레이터 설치 안됨",
            "0x31" : "유효하지 않은 맵 옵션",
            "0x32" : "유효하지 않은 차량 옵션",
            "0x33" : "네트워크 로드 오류(유요한 파일 이름이 없을때)",
            "0x34" : "네트워크 로드 오류(파일은 있지만 초기화 실패)",
            "0x35" : "센서 로드 오류(유효한 파일 이름이 없을때)",
            "0x36" : "센서 로드 오류(파일은 있지만 초기화 실패)",
            "0x37" : "시나리오 로드 오류"
        }

        ##Launcher_Command
        self.dict_launcher_command={
            "0x0000" : "명령없음",
            "0x0001" : "로그인 명령",
            "0x0002" : "시뮬레이터 선택 명령",
            "0x0003" : "시뮬레이터 설치 명령",
            "0x0004" : "시뮬레이터 실행 명령",
            "0x1000" : "런처 종료 명령",
            "0x1001" : "런처 로그아웃",
            "0x0012" : "센서 데이터 세팅 명령"
            
        }
        
        ##Simulator_Command
        self.dict_simulator_command={
            "0x0000" : "명령없음",
            "0x0001" : "시뮬레이션/옵션 변경 실행 명령",
            "0x0002" : "시뮬레이션 Pause",
            "0x0003" : "시뮬레이션 Play",
            "0x0011" : "네트워크 데이터 세팅 명령",
            "0x0012" : "센서 데이터 세팅 명령",
            "0x0013" : "시나리오 데이터 세팅 명령",
            "0x0014" : "시나리오 데이터 저장 명령",
            "0x0015" : "센서 데이터 저장 명령",
            "0x0016" : "네트워크 데이터 저장 명령",    
            "0x1000" : "시뮬레이터 종료 명령"            
        }


    def print_info(self,status_data):        

        self.platform, self.stage, self.status, self.cmd_platform, self.cmd, self.cmd_option, self.result = status_data
        
        self.is_wait = '0x1000'        
        
        print("Data_Platform = {}".format(self.dict_data_platform[self.platform]))
        if self.platform == Platform.LUANCHER:
            print("Data_Stage = {}".format(self.dict_data_launcher_stage[self.stage]))
            if self.dict_data_launcher_stage[self.stage] == Stage.BEFORE_LOGIN:
                if int(self.is_wait,16) < int(self.status,16):
                    print("Data_Status = Wait_status")
                else:
                    print("Data_Status = {}".format(self.dict_data_launcher_status1[self.status]))
            else :
                if int(self.is_wait,16) < int(self.status,16):
                    print("Data_Status = Wait_status")
                else:
                    print("Data_Status = {}".format(self.dict_data_launcher_status2[self.status]))
            
        else:
            print("Data_Stage = {}".format(self.dict_data_simulator_stage[self.stage]))
            
            if self.stage == Stage.LOBBY:                
                if int(self.is_wait,16) < int(self.status,16):
                    print("Data_Status = Wait_status")
                else:
                    print("Data_Status = {}".format(self.dict_data_simulator_status1[self.status]))

            else:
                if int(self.is_wait,16) < int(self.status,16):
                    print("Data_Status = Wait_status")
                else:
                    print("Data_Status = {}".format(self.dict_data_simulator_status2[self.status]))
        #-------------------------------------------------------------------------------------------#
        if not self.cmd=="0x0000":
            print("Command_Platform = {}".format(self.dict_data_platform[self.cmd_platform]))
            if self.cmd_platform == Platform.LUANCHER:
                print("Command_Cmd = {}".format(self.dict_launcher_command[self.cmd]))
            else:
                print("Command_Cmd = {}".format(self.dict_simulator_command[self.cmd]))
                
            if self.cmd_platform=="0x01" and self.cmd =="0x0001" :

                print("Command_Option = "+"*"*len(self.cmd_option))
            else:
                print("Command_Option = {}".format(self.cmd_option))

            print("Command_Result = {}".format(self.dict_result[self.result]))
        
        print("------------------------------")
            









