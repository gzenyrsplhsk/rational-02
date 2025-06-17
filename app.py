# 필요한 라이브러리 임포트
import streamlit as st
import json
import time
import random
import os
import base64
from openai import OpenAI
import streamlit_javascript as st_js # streamlit_javascript 임포트

# OpenAI API 키 설정 (필요시 사용)
client = None
if os.getenv('OPENAI_API_KEY'):
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    except Exception as e:
        st.error(f"OpenAI API 클라이언트 초기화 오류: {e}")
else:
    pass

# SDGs 목표 리스트 정의 (해결 방안 추가)
SDGS = [
    {"id": 1, "name": "빈곤 퇴치", "description": "모든 곳에서 빈곤을 종식시킨다.", "target": 1000, "solutions": [
        "공정 무역 제품 구매하기", "지역사회 자선단체에 기부하기", "빈곤 문제 인식 캠페인 참여하기",
        "소액 대출 프로그램 지원하기", "취약 계층에게 재능 기부하기"
    ]},
    {"id": 2, "name": "기아 종식", "description": "기아 종식을 달성하고 식량 안보를 보장한다.", "target": 800, "solutions": [
        "음식물 쓰레기 줄이기", "지역 농산물 소비하기", "푸드 뱅크에 식품 기부하기",
        "지속가능한 농업 지지하기", "굶주린 사람들을 위한 모금 활동 참여하기"
    ]},
    {"id": 3, "name": "건강과 복지", "description": "모든 사람의 건강한 삶을 보장한다.", "target": 900, "solutions": [
        "규칙적인 운동과 건강한 식단 유지하기", "지역 보건 캠페인 참여하기", "의료 취약 계층 돕기",
        "정신 건강 인식 개선에 기여하기", "예방 접종의 중요성 알리기"
    ]},
    {"id": 4, "name": "질 높은 교육", "description": "포용적이고 공정한 교육을 제공한다.", "target": 700, "solutions": [
        "교육 기부 프로그램 참여하기", "저소득층 학생 멘토링하기", "평생 교육의 중요성 홍보하기",
        "공공 도서관 이용 활성화에 기여하기", "학교 시설 개선을 위한 자원봉사"
    ]},
    {"id": 5, "name": "성평등", "description": "성평등을 달성하고 여성의 권한을 강화한다.", "target": 600, "solutions": [
        "성차별적 언행 지양하기", "성평등 관련 정책 지지하기", "여성 교육 및 취업 기회 확대 옹호하기",
        "가정 내 성 역할 고정관념 깨기", "성폭력 예방 교육 참여하기"
    ]},
    {"id": 6, "name": "깨끗한 물", "description": "모두를 위한 물과 위생을 보장한다.", "target": 800, "solutions": [
        "물 절약 습관 생활화하기", "하천 오염 방지 캠페인 참여하기", "정수 시설 개선 지원하기",
        "화학 물질 사용 줄이기", "빗물 활용 시스템 구축 고려하기"
    ]},
    {"id": 7, "name": "지속가능한 에너지", "description": "모두를 위한 지속가능한 에너지를 제공한다.", "target": 700, "solutions": [
        "에너지 절약형 가전제품 사용하기", "대중교통 이용 늘리기", "재생 에너지 도입 지지하기",
        "불필요한 전등 끄기", "자전거 이용 생활화하기"
    ]},
    {"id": 8, "name": "일자리와 경제성장", "description": "지속가능한 경제 성장을 촉진한다.", "target": 900, "solutions": [
        "지역 소상공인 제품 구매하기", "사회적 기업 활동 지지하기", "취약 계층 자립 지원 프로그램 참여하기",
        "공정한 노동 환경 조성에 관심 갖기", "청년 창업 지원 멘토링"
    ]},
    {"id": 9, "name": "산업과 혁신", "description": "탄력적인 인프라와 지속가능한 산업화를 촉진한다.", "target": 600, "solutions": [
        "친환경 기술 개발에 투자 지지하기", "재활용 가능한 제품 사용하기", "스마트 도시 조성에 관심 갖기",
        "지속가능한 건축 자재 선택하기", "혁신적인 재활용 시스템 아이디어 제안"
    ]},
    {"id": 10, "name": "불평등 감소", "description": "국가 내 및 국가 간 불평등을 줄인다.", "target": 700, "solutions": [
        "다문화 이해 교육 참여하기", "장애인 차별 철폐에 동참하기", "이주민 인권 옹호 활동 지지하기",
        "소수자 목소리에 귀 기울이기", "공정한 세금 정책 지지"
    ]},
    {"id": 11, "name": "지속가능한 도시", "description": "도시를 포용적이고 안전하게 만든다.", "target": 800, "solutions": [
        "대중교통 활성화에 기여하기", "도심 녹지 공간 확대 지지하기", "안전한 보행 환경 조성에 참여하기",
        "주민 참여형 도시 계획에 관심 갖기", "자원 순환형 도시 모델 제안"
    ]},
    {"id": 12, "name": "지속가능한 소비", "description": "지속가능한 소비와 생산 패턴을 보장한다.", "target": 600, "solutions": [
        "친환경 제품 구매하기", "과도한 포장 제품 피하기", "일회용품 사용 줄이기",
        "업사이클링/리사이클링 활동 참여하기", "에너지 효율 등급 높은 제품 선택하기"
    ]},
    {"id": 13, "name": "기후 행동", "description": "기후 변화에 대한 즉각적인 조치를 취한다.", "target": 1000, "solutions": [
        "탄소 발자국 줄이기", "나무 심기 캠페인 참여하기", "재생 에너지 전환 지지하기",
        "기후 변화 교육 확산에 기여하기", "온실가스 감축을 위한 생활 습관 실천"
    ]},
    {"id": 14, "name": "해양 생태계", "description": "해양 자원을 보존하고 지속가능하게 사용한다.", "target": 800, "solutions": [
        "해양 플라스틱 사용 줄이기", "해변 정화 활동 참여하기", "지속가능한 수산물 소비하기",
        "바다 생물 보호 캠페인 지지하기", "미세 플라스틱 없는 제품 사용"
    ]},
    {"id": 15, "name": "육상 생태계", "description": "육상 생태계를 보호하고 복원한다.", "target": 700, "solutions": [
        "멸종 위기 동물 보호 활동 참여하기", "숲 보호 및 복원 프로젝트 지원하기", "산림 훼손 방지 노력",
        "불법 벌목 및 밀렵 반대하기", "친환경적인 농업 방식 지지하기"
    ]},
    {"id": 16, "name": "평화와 정의", "description": "평화롭고 포용적인 사회를 촉진한다.", "target": 900, "solutions": [
        "차별과 혐오 표현 반대하기", "분쟁 지역 난민 돕기", "투명하고 책임 있는 정부 지지하기",
        "평화 교육 확산에 기여하기", "인권 옹호 활동 참여하기"
    ]},
    {"id": 17, "name": "파트너십", "description": "지속가능한 발전을 위한 글로벌 파트너십을 강화한다.", "target": 600, "solutions": [
        "SDGs 관련 단체 후원하기", "글로벌 협력 프로젝트에 관심 갖기", "국제 교류 프로그램 참여하기",
        "기업의 사회적 책임 활동 지지하기", "다양한 이해관계자와 협력 모색"
    ]},
    {"id": 18, "name": "종합적 지속가능성", "description": "모든 SDGs의 통합적 달성을 목표로 한다.", "target": 1200, "solutions": [
        "모든 SDGs를 통합적으로 이해하고 실천하기", "지속가능한 삶의 방식 전파하기",
        "다양한 분야의 전문가와 협력하기", "지속가능성 교육 프로그램 개발에 참여하기",
        "개인의 작은 실천이 모여 큰 변화를 만든다는 믿음 가지기"
    ]}
]

# 마스터 모드 비밀번호 (JavaScript에서 바로 사용되지 않음, Python에서 확인)
MASTER_PASSWORD = "8729"

# Streamlit 세션 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "earth_level": 0,
        "recovery_points": 0,
        "contribution_points": [0] * len(SDGS),
        "achievements": [0] * len(SDGS),
        "difficulty": 1,
        "endings_seen": 0,
        "start_time": time.time(),
        "game_mode": "normal",
        "completed_sdgs": set(),
        "history": [],
        "player_name": "",
        "master_mode_active": False,
        "master_password_entered": False # 비밀번호 입력 여부
    }

# 마스터 모드 키 감지 JavaScript 삽입
# 이 코드는 앱이 로드될 때 한 번만 실행되도록 singleton=True 설정
# / 키 두 번 감지 시 session_state.master_key_pressed를 True로 설정하고 rerun
js_code = """
let lastKeyPressTime = 0;
document.addEventListener('keydown', function(e) {
    if (e.key === '/' || e.key === '?') { // '/'와 '?'는 같은 키일 수 있음
        const currentTime = new Date().getTime();
        if (currentTime - lastKeyPressTime < 300) { // 300ms 이내 두 번 클릭
            if (!window.parent.streamlit_app_state) {
                console.warn("Streamlit app state not found. Cannot activate master mode.");
                return;
            }
            // Streamlit session_state 업데이트
            window.parent.streamlit_app_state.game_state.master_key_pressed = true;
            // Streamlit 앱을 새로고침하여 파이썬 코드가 변경된 세션 상태를 감지하도록 함
            window.parent.streamlit_app_state.rerun_with_query_params({});
        }
        lastKeyPressTime = currentTime;
    } else {
        lastKeyPressTime = 0; // 다른 키 누르면 초기화
    }
});
"""
st_js.st_javascript(js_code, key="master_key_listener", unsafe_allow_html=True, height=0, width=0, options={"singleton": True})


# 게임 저장 함수
def save_game():
    st.session_state.game_state["completed_sdgs"] = list(st.session_state.game_state["completed_sdgs"])
    with open("game_state.json", "w") as f:
        json.dump(st.session_state.game_state, f)
    st.success("게임이 저장되었습니다!")

# 게임 로드 함수
def load_game():
    if os.path.exists("game_state.json"):
        with open("game_state.json", "r") as f:
            st.session_state.game_state = json.load(f)
        st.session_state.game_state["completed_sdgs"] = set(st.session_state.game_state["completed_sdgs"])
        st.success("게임이 불러와졌습니다!")
    else:
        st.error("저장된 게임이 없습니다.")

# Streamlit 기반 미니게임 함수 (간단한 클릭 게임)
def play_mini_game_streamlit(sdg_index):
    st.markdown(f"### {SDGS[sdg_index]['name']} 미니게임")
    st.write("버튼을 클릭하여 점수를 획득하세요! 10초 동안 진행됩니다.")

    # 미니게임 상태 초기화
    if "minigame_start_time" not in st.session_state:
        st.session_state.minigame_start_time = time.time()
        st.session_state.minigame_points = 0
        st.session_state.minigame_active = True
        st.session_state.current_solution_text = ""

    elapsed_time = time.time() - st.session_state.minigame_start_time
    time_left = 10 - elapsed_time

    if time_left > 0 and st.session_state.minigame_active:
        st.write(f"남은 시간: {time_left:.1f}초")
        st.write(f"현재 점수: {st.session_state.minigame_points}")

        if st.session_state.current_solution_text:
            st.info(f"💡 {st.session_state.current_solution_text}")

        if st.button("클릭!"):
            if st.session_state.game_state["master_mode_active"]:
                st.session_state.minigame_points += SDGS[sdg_index]["target"] // 2 + 100
            else:
                st.session_state.minigame_points += int(10 * st.session_state.game_state["difficulty"])
            
            if SDGS[sdg_index]["solutions"]:
                st.session_state.current_solution_text = random.choice(SDGS[sdg_index]["solutions"])
            
            st.rerun()
    else:
        st.session_state.minigame_active = False
        final_points = st.session_state.minigame_points
        st.info(f"미니게임 종료! 최종 점수: {final_points}점")

        game_state = st.session_state.game_state
        game_state["contribution_points"][sdg_index] += final_points
        new_history = game_state["history"] + [f"SDG {SDGS[sdg_index]['id']} - {SDGS[sdg_index]['name']}: {final_points} 공헌점수 획득"]
        recovery_change = 0
        reason = ""

        if game_state["contribution_points"][sdg_index] >= SDGS[sdg_index]["target"] and sdg_index not in game_state["completed_sdgs"]:
            recovery_change = random.randint(5, 10)
            reason = f"{SDGS[sdg_index]['name']} 목표 달성으로 지구 회복도 +{recovery_change}%"
            game_state["completed_sdgs"].add(sdg_index)
            new_history.append(reason)

        new_earth_level = game_state["earth_level"]
        if len(game_state["completed_sdgs"]) == len(SDGS) and game_state["earth_level"] < 19:
            new_earth_level = 19
            new_history.append("모든 SDG 목표 달성! 지구 최종 강화 (+19강) 완료!")
        elif recovery_change > 0:
            new_earth_level = min(game_state["earth_level"] + 1, 19)

        game_state["recovery_points"] = min(game_state["recovery_points"] + recovery_change, 100)
        game_state["earth_level"] = new_earth_level
        game_state["history"] = new_history
        st.session_state.game_state = game_state

        if new_earth_level == 19:
            show_ending()
        
        del st.session_state.minigame_start_time
        del st.session_state.minigame_points
        del st.session_state.minigame_active
        del st.session_state.current_solution_text
        st.rerun()

def show_ending():
    game_state = st.session_state.game_state
    st.markdown("---")
    st.markdown(f"## 엔딩: 지구 회복 완료!")
    st.write(f"플레이어 **{game_state['player_name']}**님, 지구를 **+{game_state['earth_level']}강**으로 강화했습니다!")
    st.write("\n")
    st.markdown("#### 주요 활동:")
    for entry in game_state["history"]:
        st.write(f"- {entry}")
    
    st.write("\n")
    st.markdown("#### 실생활에서 할 수 있는 일:")
    for i, sdg in enumerate(SDGS):
        if game_state["contribution_points"][i] >= sdg["target"]:
            st.write(f"- **{sdg['name']}**: {random.choice(sdg['solutions'])}")

    if game_state["earth_level"] == 19:
        st.markdown("\n---")
        st.markdown("### 명예 달성!")
        st.markdown(f"**{game_state['player_name']} 영웅** - 지속가능개발목표 명예달성 시민 자격증 획득.")
        st.write("수여인: 제작자 (macu)")
        st.write(f"걸린 시간: {((time.time() - game_state['start_time']) / 3600):.2f}시간")
        st.write(f"총 공헌 점수: {sum(game_state['contribution_points'])}점")
        
        if game_state["difficulty"] == 4:
            st.success("진엔딩 달성! 모든 난이도를 클리어했습니다!")
        else:
            game_state["difficulty"] += 1
            game_state["endings_seen"] += 1
            st.warning(f"하드모드 **{game_state['difficulty']}** 오픈! 다시 도전해보세요!")
            st.session_state.game_state = game_state
        
        st.button("자격증 다운로드", on_click=download_certificate)
    st.markdown("---")


def show_achievements():
    st.markdown("---")
    st.markdown("### 도전과제")
    total_target = sum(sdg["target"] for sdg in SDGS)
    total_points = sum(st.session_state.game_state["contribution_points"])
    
    for i, sdg in enumerate(SDGS):
        progress = (st.session_state.game_state["contribution_points"][i] / sdg["target"] * 100)
        st.write(f"**{sdg['name']}**: {progress:.2f}% ({st.session_state.game_state['contribution_points'][i]}/{sdg['target']})")
        st.progress(min(progress / 100, 1.0))
    
    overall_progress = (total_points / total_target * 100) if total_target > 0 else 0
    st.markdown(f"\n**총 달성률**: {overall_progress:.2f}%")
    st.progress(min(overall_progress / 100, 1.0))
    st.markdown("---")


def download_certificate():
    game_state = st.session_state.game_state
    certificate_text = f"""
---
지속가능개발목표 명예달성 시민 자격증
---

수여자: {game_state['player_name']}

당신은 지구 회복을 위한 헌신과 노고를 통해 
지속가능개발목표(SDGs) 달성에 크게 기여하였으므로,
이 명예 자격증을 수여합니다.

수여일: {time.strftime('%Y-%m-%d')}
총 공헌 점수: {sum(game_state['contribution_points'])}점
소요 시간: {((time.time() - game_state['start_time']) / 3600):.2f}시간

수여인: 제작자 (macu)

---
"""
    b64 = base64.b64encode(certificate_text.encode("utf-8")).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{game_state["player_name"]}_SDGs_Certificate.txt">자격증 다운로드</a>'
    st.markdown(href, unsafe_allow_html=True)

def reset_game():
    st.session_state.game_state = {
        "earth_level": 0,
        "recovery_points": 0,
        "contribution_points": [0] * len(SDGS),
        "achievements": [0] * len(SDGS),
        "difficulty": 1,
        "endings_seen": 0,
        "start_time": time.time(),
        "game_mode": "normal",
        "completed_sdgs": set(),
        "history": [],
        "player_name": st.session_state.game_state["player_name"],
        "master_mode_active": False,
        "master_password_entered": False
    }
    st.success("게임이 초기화되었습니다!")
    st.rerun()

def main():
    st.title("🌍 지구 회복 타이쿤")

    # 마스터 모드 활성화 로직
    if "master_key_pressed" in st.session_state.game_state and st.session_state.game_state["master_key_pressed"]:
        st.session_state.game_state["master_key_pressed"] = False # 플래그 초기화
        st.session_state.game_state["master_password_entered"] = True # 비밀번호 입력 상태로 전환
        st.info("비밀번호 입력 창이 나타났습니다.")
        st.rerun() # 비밀번호 입력창을 바로 띄우기 위해 리런

    if st.session_state.game_state["master_password_entered"] and not st.session_state.game_state["master_mode_active"]:
        password_input = st.text_input("마스터 모드 비밀번호를 입력하세요.", key="master_password_input", type="password")
        if password_input == MASTER_PASSWORD:
            st.session_state.game_state["master_mode_active"] = True
            st.session_state.game_state["master_password_entered"] = False # 비밀번호 입력 상태 초기화
            st.success("⭐ 마스터 모드가 활성화되었습니다! ⭐")
            st.toast("모든 SDG 목표 달성치가 50%로 설정됩니다. 이제 2번의 클릭으로 목표 달성 가능!")
            for i in range(len(SDGS)):
                st.session_state.game_state["contribution_points"][i] = SDGS[i]["target"] // 2
            st.rerun()
        elif password_input: # 비밀번호를 입력했지만 틀렸을 경우
            st.error("잘못된 비밀번호입니다.")
            st.session_state.game_state["master_password_entered"] = False # 다시 대기 상태로
            st.rerun()
    elif st.session_state.game_state["master_mode_active"]:
        st.sidebar.success("⭐ 마스터 모드 활성화됨 ⭐")

    # 게임 시작 전 이름 입력
    if not st.session_state.game_state["player_name"]:
        st.markdown("---")
        st.subheader("새로운 여정을 시작합니다!")
        player_name = st.text_input("4글자 플레이어 이름을 입력하세요.", max_chars=4)
        if st.button("게임 시작"):
            if len(player_name) == 4:
                st.session_state.game_state["player_name"] = player_name
                st.success(f"{player_name}님, 게임을 시작합니다!")
                st.rerun()
            else:
                st.error("이름은 반드시 4글자여야 합니다!")
        st.markdown("---")
        return

    game_state = st.session_state.game_state
    
    st.sidebar.header("게임 현황")
    st.sidebar.write(f"**플레이어**: {game_state['player_name']}")
    st.sidebar.write(f"**현재 난이도**: {game_state['difficulty']}")
    st.sidebar.progress(game_state['recovery_points'] / 100.0, text=f"**지구 회복도**: {game_state['recovery_points']}%")
    st.sidebar.write(f"**지구 강화**: +{game_state['earth_level']}강")
    
    if "minigame_active" not in st.session_state or not st.session_state.minigame_active:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 게임 저장"):
                save_game()
        with col2:
            if st.button("🔄 이어하기"):
                load_game()
        with col3:
            if st.button("☠️ 다시하기"):
                reset_game()

        st.markdown("---")
        if st.button("🏆 도전과제 보기"):
            show_achievements()
        st.markdown("---")

        st.subheader("지속가능개발목표(SDGs) 목록")
        for i, sdg in enumerate(SDGS):
            st.markdown(f"#### SDG {sdg['id']}: {sdg['name']}")
            st.write(f"**설명**: {sdg['description']}")
            current_points = game_state['contribution_points'][i]
            target_points = sdg['target']
            progress_percent = (current_points / target_points * 100) if target_points > 0 else 0
            
            st.write(f"**공헌 점수**: {current_points}/{target_points} ({progress_percent:.2f}%)")
            st.progress(min(progress_percent / 100, 1.0))

            if i in game_state["completed_sdgs"]:
                st.success(f"✔️ {sdg['name']} 목표 달성!")
            else:
                if st.button(f"✨ {sdg['name']} 미니게임 플레이!", key=f"minigame_start_{i}"):
                    st.session_state.current_sdg_index = i
                    st.session_state.minigame_start_time = time.time()
                    st.session_state.minigame_points = 0
                    st.session_state.minigame_active = True
                    st.rerun()
            st.markdown("---")
    else:
        play_mini_game_streamlit(st.session_state.current_sdg_index)

    if game_state["earth_level"] == 19:
        show_ending()
    
    # 맨 아래에 'made by macu' 문구 추가
    st.markdown("<p style='text-align: center; font-size: 0.8em; color: grey;'>made by macu</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
