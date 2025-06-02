import streamlit as st
import json
import os
from collections import Counter

# --- Constants ---
# 작업자 목록
WORKERS = ['지오', '성민', '용범']
# CS Level 옵션
CS_LEVELS = ['word', 'phrase', 'sentence']
# 주요 언어 옵션
MAIN_LANGUAGES = ['English', 'Korean']
# 카테고리 목록
CATEGORIES = [
    "business",
    "everyday conversation",
    "language education",
    "entertainment",
    "slang/neologisms",
    "travel",
    "software development",
    "medical",
    "academic",
    "traditional culture"
]
SCRIPT_FILE_PREFIX = "scripts_"
SCRIPT_FILE_SUFFIX = ".json"

# --- Helper Functions ---

def get_script_filename(worker_name):
    """작업자 이름에 해당하는 스크립트 파일명을 반환합니다."""
    return f"{SCRIPT_FILE_PREFIX}{worker_name}{SCRIPT_FILE_SUFFIX}"

def load_scripts(worker_name):
    """지정된 작업자의 스크립트 파일을 로드합니다."""
    filename = get_script_filename(worker_name)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                scripts = json.load(f)
                # 파일 내용이 리스트가 아니면 빈 리스트 반환
                if not isinstance(scripts, list):
                    st.warning(f"{filename} 파일의 내용이 올바른 리스트 형식이 아닙니다. 빈 목록으로 시작합니다.")
                    return []
                return scripts
        except json.JSONDecodeError:
            st.error(f"{filename} 파일이 올바른 JSON 형식이 아닙니다. 빈 목록으로 시작합니다.")
            return []
        except Exception as e:
            st.error(f"{filename} 파일 로드 중 오류 발생: {e}")
            return []
    return []

def save_scripts(worker_name, scripts_data):
    """지정된 작업자의 스크립트 데이터를 파일에 저장합니다."""
    filename = get_script_filename(worker_name)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(scripts_data, f, ensure_ascii=False, indent=2)
        # st.success(f"{filename}에 스크립트가 성공적으로 저장되었습니다.") # 너무 자주 표시될 수 있어 주석 처리
    except Exception as e:
        st.error(f"스크립트 저장 중 오류 발생: {e}")

# --- Page Functions ---

def login_page():
    """작업자 선택 페이지를 표시합니다."""
    st.set_page_config(layout="wide", page_title="오디오 스크립트 도구")
    st.title("🎙️ 오디오 스크립트 작성 도구")
    st.header("작업자 선택")

    # st.session_state에서 이전에 선택한 작업자 이름을 가져오거나 기본값 사용
    # 로그인 페이지에서는 선택을 초기화하기 위해 기본값을 빈 문자열로 설정
    selected_worker_index = 0 # 기본적으로 "선택하세요"
    # 이전에 선택한 작업자가 있다면 해당 작업자를 기본값으로 설정할 수 있으나,
    # 로그인 페이지에서는 보통 새로 선택하게 하므로, 빈 문자열로 시작하는 것이 나을 수 있습니다.
    # 예: if 'login_selectbox_value' in st.session_state:
    #         try: selected_worker_index = ([""] + WORKERS).index(st.session_state.login_selectbox_value)
    #         except ValueError: selected_worker_index = 0


    selected_worker = st.selectbox(
        "이름을 선택하세요:",
        options=[""] + WORKERS,  # 첫 번째 옵션으로 빈 문자열 추가
        index=selected_worker_index,
        key="login_worker_select"
    )
    
    # st.session_state.login_selectbox_value = selected_worker # 현재 선택된 값을 저장 (선택 사항)

    if selected_worker: # 빈 문자열이 아닌 작업자가 선택된 경우
        if st.button("작업 시작", key="start_work_button", type="primary"):
            st.session_state.worker_name = selected_worker
            st.session_state.scripts = load_scripts(selected_worker)
            st.session_state.page = "work"
            st.rerun()
    else:
        st.info("목록에서 작업자 이름을 선택 후 '작업 시작' 버튼을 눌러주세요.")


def work_page():
    """스크립트 작성 작업 페이지를 표시합니다."""
    st.set_page_config(layout="wide", page_title=f"{st.session_state.get('worker_name', '작업')} 페이지")

    if 'worker_name' not in st.session_state or not st.session_state.worker_name:
        st.session_state.page = "login" # 작업자 정보가 없으면 로그인 페이지로
        st.rerun()
        return

    worker_name = st.session_state.worker_name
    st.title(f"📝 {worker_name}님, 안녕하세요!")
    st.subheader("스크립트 작업 공간")

    # --- Sidebar for file operations and stats ---
    with st.sidebar:
        st.header("파일 작업")
        
        # 파일 업로드
        # key를 worker_name과 연결하여 작업자 변경 시 uploader 상태가 초기화되도록 유도
        uploaded_file = st.file_uploader(
            "스크립트 파일 업로드 (.json)",
            type="json",
            key=f"uploader_{worker_name}"
        )
        if uploaded_file is not None:
            try:
                uploaded_data = json.load(uploaded_file)
                if isinstance(uploaded_data, list):
                    # 모든 항목이 딕셔너리인지, 필요한 키를 가지고 있는지 등 추가 검증 가능
                    st.session_state.scripts = uploaded_data
                    save_scripts(worker_name, st.session_state.scripts)
                    st.success("파일이 성공적으로 업로드 및 저장되었습니다. 페이지가 새로고침됩니다.")
                    st.rerun() # 업로드 후 UI 즉시 업데이트
                else:
                    st.error("업로드된 파일이 리스트 형태의 JSON이 아닙니다.")
            except json.JSONDecodeError:
                st.error("업로드된 파일이 올바른 JSON 형식이 아닙니다.")
            except Exception as e:
                st.error(f"파일 업로드 처리 중 오류: {e}")

        # 파일 다운로드
        if st.session_state.get('scripts'): # 스크립트가 있을 때만 다운로드 버튼 표시
            try:
                scripts_json = json.dumps(st.session_state.scripts, ensure_ascii=False, indent=2)
                st.download_button(
                    label="현재 스크립트 다운로드",
                    data=scripts_json,
                    file_name=get_script_filename(worker_name),
                    mime="application/json",
                    key="download_button"
                )
            except Exception as e:
                st.error(f"다운로드 파일 생성 중 오류: {e}")
        else:
            st.info("다운로드할 스크립트가 없습니다.")

        st.divider()
        st.header("카테고리별 스크립트 수")
        if st.session_state.get('scripts'):
            category_counts = Counter(script.get('category', 'N/A') for script in st.session_state.scripts)
            for category_item in CATEGORIES:
                st.markdown(f"- **{category_item}:** {category_counts.get(category_item, 0)}")
            if category_counts.get('N/A', 0) > 0: # 'N/A' 카테고리가 있는 경우 (이론상 없어야 함)
                 st.markdown(f"- **(카테고리 없음):** {category_counts['N/A']}")
        else:
            st.write("아직 작성된 스크립트가 없습니다.")
        
        st.divider()
        if st.button("작업자 변경 (로그아웃)", key="change_worker_button"):
            # 현재 작업 내용 저장 여부 확인은 생략 (자동 저장 로직 사용 중)
            st.session_state.page = "login"
            # 작업자 관련 세션 상태 초기화
            keys_to_clear = ['worker_name', 'scripts'] 
            for key_to_del in keys_to_clear:
                if key_to_del in st.session_state:
                    del st.session_state[key_to_del]
            st.rerun()

    # --- Main content for script input ---
    st.subheader("➕ 새 스크립트 추가")
    # clear_on_submit=True는 form 제출 후 입력 필드를 초기화합니다.
    with st.form(key="script_form", clear_on_submit=True):
        text = st.text_area("스크립트 내용 (Text):", key="text_input", height=100, placeholder="여기에 스크립트 내용을 입력하세요...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cs_level = st.selectbox("CS Level:", CS_LEVELS, key="cs_level_select")
        with col2:
            main_lang = st.selectbox("Main Language:", MAIN_LANGUAGES, key="main_lang_select")
        with col3:
            category = st.selectbox("Category:", CATEGORIES, key="category_select")
        
        submit_button = st.form_submit_button(label="✅ 스크립트 추가하기")

    if submit_button:
        if not text.strip():
            st.warning("스크립트 내용을 입력해주세요.", icon="⚠️")
        else:
            new_script = {
                "text": text,
                "cs-level": cs_level,
                "main": main_lang,
                "category": category
            }
            # st.session_state.scripts가 없을 경우를 대비 (이론상 login 시 초기화됨)
            if 'scripts' not in st.session_state or st.session_state.scripts is None:
                st.session_state.scripts = []
            st.session_state.scripts.append(new_script)
            save_scripts(worker_name, st.session_state.scripts) # 추가 시 즉시 저장
            st.success("스크립트가 성공적으로 추가 및 저장되었습니다!", icon="🎉")
            st.rerun() # UI 업데이트 (카테고리 카운트, 스크립트 목록)

    st.divider()

    # --- Display existing scripts ---
    st.subheader("📋 작성된 스크립트 목록")
    if st.session_state.get('scripts'):
        # 스크립트 목록을 최신순으로 표시 (reversed)
        scripts_to_display = list(reversed(st.session_state.scripts))
        
        for i, script_data in enumerate(scripts_to_display):
            original_index = len(st.session_state.scripts) - 1 - i # 원본 리스트에서의 인덱스
            
            with st.expander(f"스크립트 #{original_index + 1} : {script_data.get('text', '')[:60]}...", expanded=False):
                st.json(script_data) # 스크립트 내용 전체 보기
                
                # 스크립트 삭제 버튼
                if st.button(f"🗑️ 스크립트 #{original_index + 1} 삭제", key=f"delete_script_{original_index}", type="secondary"):
                    # 삭제 확인 절차 (선택 사항)
                    # confirm_delete = st.checkbox(f"정말로 스크립트 #{original_index + 1}을(를) 삭제하시겠습니까?", key=f"confirm_delete_{original_index}")
                    # if confirm_delete:
                    st.session_state.scripts.pop(original_index) # 원본 인덱스로 삭제
                    save_scripts(worker_name, st.session_state.scripts) # 삭제 후 즉시 저장
                    st.success(f"스크립트 #{original_index + 1}이(가) 삭제되었습니다.")
                    st.rerun() # UI 업데이트
    else:
        st.info("아직 추가된 스크립트가 없습니다. 위 양식을 사용하여 새 스크립트를 추가해보세요.")


# --- Main App Logic ---
def main():
    """애플리케이션 메인 로직을 실행합니다."""
    # 세션 상태 변수 초기화 (최초 실행 시)
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'scripts' not in st.session_state: # 현재 작업자의 스크립트 목록
        st.session_state.scripts = []
    if 'worker_name' not in st.session_state: # 현재 작업자 이름
        st.session_state.worker_name = None

    # 페이지 라우팅
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "work":
        work_page()
    else: # 예외 처리: 알 수 없는 페이지 상태면 로그인 페이지로
        st.session_state.page = "login"
        login_page()

if __name__ == "__main__":
    main()
