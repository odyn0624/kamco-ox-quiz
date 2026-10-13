import random

import streamlit as st

# ─────────────────────────────────────────
# 0. 페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(page_title="캠코 생활금융 OX", page_icon="🐹", layout="centered")

KAMCO_URL = "https://www.kamco.or.kr"
ONBID_URL = "https://www.onbid.co.kr"

# ─────────────────────────────────────────
# 1. 문제 데이터 (q: 문제, a: 정답, exp: 해설)
# ─────────────────────────────────────────
QUESTIONS = [
    {"q": "공매와 경매는 같은 말이다.", "a": "X",
     "exp": "공매는 세금 체납으로 압류된 재산을 캠코가 대신 파는 것(국세징수법)이고, 경매는 법원이 진행해요(민사집행법)."},
    {"q": "나라 땅을 허가 없이 쓰다 걸리면 정식으로 빌린 사람보다 돈을 더 낸다.", "a": "O",
     "exp": "대부료의 120%를 변상금으로 내고, 최대 5년치까지 소급돼요."},
    {"q": "캠코 채무조정에서는 담보 없는 빚의 '원금'도 줄여줄 수 있다.", "a": "O",
     "exp": "무담보 채권은 원금을 30~60%(사회취약계층은 최대 90%)까지 감면하고, 이자는 전액 감면해요."},
    {"q": "세금을 안 낸 사람의 재산을 압류하는 곳은 캠코다.", "a": "X",
     "exp": "압류는 세무서나 지자체가 해요. 캠코는 압류된 재산을 파는 일을 대행해요."},
    {"q": "온비드에서는 압류재산 공매만 할 수 있다.", "a": "X",
     "exp": "국유재산 매각·대부 입찰도 온비드에서 진행돼요."},
    {"q": "나라 땅을 팔 때는 원칙적으로 공개경쟁입찰로 판다.", "a": "O",
     "exp": "공개경쟁입찰이 원칙이고, 법령에 정한 경우에만 수의계약이 가능해요."},
    {"q": "나라 땅을 사면 대금을 무조건 한 번에 내야 한다.", "a": "X",
     "exp": "3천만 원 이하는 3년, 3천만 원 초과는 5년 이내로 나눠 낼 수 있어요."},
    {"q": "캠코는 체납 세금을 걷으려고 체납자의 재산을 직접 강제로 팔 수 있다.", "a": "X",
     "exp": "캠코는 소재 파악, 납부 안내, 재산조사까지만 해요. 강제징수는 세무서가 해요."},
    {"q": "빚진 본인뿐 아니라 연대보증인이나 상속인도 채무조정을 신청할 수 있다.", "a": "O",
     "exp": "주채무자, 연대보증인, 상속인 모두 신청할 수 있어요."},
    {"q": "나라 재산 중 빌려주거나 팔 수 있는 건 '일반재산'이다.", "a": "O",
     "exp": "국가가 직접 쓰는 재산은 '행정재산', 나머지가 '일반재산'이에요. 일반재산은 대부하거나 매각할 수 있어요."},
]

# ─────────────────────────────────────────
# 2. 결과 데이터 (min~max 점수 구간별)
# ─────────────────────────────────────────
RESULTS = [
    {"min": 0, "max": 2, "emoji": "🥔", "name": "아직 감자 상태인 햄찌",
     "line": "흐엥… 온비드가 먹는 건 줄 알았어…",
     "traits": ["공매를 '공짜 매장'으로 앎", "변상금 120% 듣고 \"세일인가?\" 함", "그래도 끝까지 푼 근성은 만점"],
     "tip": "빚이 부담된다면 혼자 고민하지 말고 캠코 채무조정부터 알아보기",
     "link_label": "캠코 홈페이지 가기", "link": KAMCO_URL, "effect": "snow"},
    {"min": 3, "max": 4, "emoji": "🐹", "name": "볼주머니에 상식 저장 중인 채람쥐",
     "line": "조금 알 것 같기도… 아닌 것 같기도…!",
     "traits": ["들어본 단어는 많은데 설명은 못 함", "\"경매랑 공매? 비슷한 거 아냐?\"", "성장 가능성 무한대"],
     "tip": "공매와 경매는 달라요! 공매 물건은 온비드에서 볼 수 있어요",
     "link_label": "온비드 구경하기", "link": ONBID_URL, "effect": None},
    {"min": 5, "max": 6, "emoji": "🐰", "name": "눈치로 버티는 토깽이 인턴",
     "line": "반은 맞았으니까… 반은 인턴이야…!",
     "traits": ["찍은 것도 맞힌 걸로 치는 긍정왕", "회의 때 고개를 제일 열심히 끄덕임", "조금만 더 하면 정규직 각"],
     "tip": "연대보증인·상속인도 채무조정을 신청할 수 있어요",
     "link_label": "캠코 홈페이지 가기", "link": KAMCO_URL, "effect": None},
    {"min": 7, "max": 8, "emoji": "🐱", "name": "공매 고수 지냥선배",
     "line": "후후… 압류는 세무서, 공매는 캠코다냥.",
     "traits": ["친구 자취방 계약할 때 불려감", "온비드 즐겨찾기 해 둠", "\"그건 행정재산이라 안 돼\" 가능"],
     "tip": "나라 땅도 공개입찰로 살 수 있고, 대금은 나눠 낼 수 있어요",
     "link_label": "온비드 구경하기", "link": ONBID_URL, "effect": "balloons"},
    {"min": 9, "max": 10, "emoji": "🐻👑", "name": "전설의 국유재산 수호곰",
     "line": "이 땅은… 내가 지킨다.",
     "traits": ["캠코 직원보다 캠코를 잘 앎(?)", "길 가다 빈 땅 보면 \"일반재산인가…\" 중얼거림", "지금 바로 캠코 지원서 쓰러 가야 함"],
     "tip": "이 지식을 주변에 공유해서 생활금융 수호곰을 늘려 주세요!",
     "link_label": "캠코 홈페이지 가기", "link": KAMCO_URL, "effect": "balloons"},
]

CORRECT_REACTIONS = ["히히 맞았다🎉", "천재 아니야?!", "볼주머니 +1 🐹"]
WRONG_REACTIONS = ["앗… 괜찮아…🥲", "흐엥 틀렸어…", "다음 건 맞힐 수 있어…!"]

# ─────────────────────────────────────────
# 3. 상태 저장 (Streamlit은 버튼을 누를 때마다 코드를 처음부터 다시 실행하므로
#    점수·문제 번호 같은 값은 session_state에 보관해야 해요)
# ─────────────────────────────────────────
def reset():
    st.session_state.page = "start"   # start → quiz → result
    st.session_state.idx = 0          # 지금 몇 번 문제인지
    st.session_state.score = 0        # 맞힌 개수
    st.session_state.answers = []     # 내가 고른 답 목록
    st.session_state.answered = False # 지금 문제에 답했는지
    st.session_state.reaction = ""
    st.session_state.effect_shown = False


if "page" not in st.session_state:
    reset()


def start_quiz():
    st.session_state.page = "quiz"


def choose(choice):
    q = QUESTIONS[st.session_state.idx]
    st.session_state.answers.append(choice)
    if choice == q["a"]:
        st.session_state.score += 1
        st.session_state.reaction = random.choice(CORRECT_REACTIONS)
    else:
        st.session_state.reaction = random.choice(WRONG_REACTIONS)
    st.session_state.answered = True


def next_question():
    st.session_state.idx += 1
    st.session_state.answered = False
    if st.session_state.idx >= len(QUESTIONS):
        st.session_state.page = "result"


def get_result(score):
    for r in RESULTS:
        if r["min"] <= score <= r["max"]:
            return r


# ─────────────────────────────────────────
# 4. 화면 ① 시작
# ─────────────────────────────────────────
if st.session_state.page == "start":
    st.markdown("<h1 style='text-align:center'>캠코 생활금융 OX 🐹</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px'>공매? 채무조정? 국유재산?<br>"
                "10문제로 알아보는 나의 생활금융 레벨!</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:60px'>🥔 🐹 🐰 🐱 🐻</p>", unsafe_allow_html=True)
    st.button("시작하기 🚀", on_click=start_quiz, width="stretch", type="primary")

# ─────────────────────────────────────────
# 5. 화면 ② 퀴즈
# ─────────────────────────────────────────
elif st.session_state.page == "quiz":
    i = st.session_state.idx
    q = QUESTIONS[i]

    st.progress((i + 1) / len(QUESTIONS), text=f"{i + 1} / {len(QUESTIONS)}")
    st.markdown(f"### Q{i + 1}. {q['q']}")

    if not st.session_state.answered:
        col1, col2 = st.columns(2)
        col1.button("⭕", on_click=choose, args=("O",), width="stretch")
        col2.button("❌", on_click=choose, args=("X",), width="stretch")
    else:
        if st.session_state.answers[-1] == q["a"]:
            st.success(f"**{st.session_state.reaction}**  정답은 {q['a']}!")
        else:
            st.error(f"**{st.session_state.reaction}**  정답은 {q['a']}!")
        st.info(f"💡 {q['exp']}")
        label = "결과 보기 🎁" if i == len(QUESTIONS) - 1 else "다음 문제 ▶"
        st.button(label, on_click=next_question, width="stretch", type="primary")

# ─────────────────────────────────────────
# 6. 화면 ③ 결과
# ─────────────────────────────────────────
elif st.session_state.page == "result":
    score = st.session_state.score
    r = get_result(score)

    if not st.session_state.effect_shown:
        if r["effect"] == "balloons":
            st.balloons()
        elif r["effect"] == "snow":
            st.snow()
        st.session_state.effect_shown = True

    st.markdown(f"<p style='text-align:center; font-size:20px'>10문제 중 <b>{score}개</b> 맞혔어요!</p>",
                unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:90px; margin:0'>{r['emoji']}</p>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center'>{r['name']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:18px'>\"{r['line']}\"</p>", unsafe_allow_html=True)

    st.markdown("#### 🔍 이런 특징이 있어요")
    for t in r["traits"]:
        st.markdown(f"- {t}")

    st.markdown("#### 🍯 오늘의 생활금융 꿀팁")
    st.success(r["tip"])
    st.link_button(r["link_label"], r["link"], width="stretch")

    wrong = [(n, q) for n, q in enumerate(QUESTIONS) if st.session_state.answers[n] != q["a"]]
    if wrong:
        with st.expander(f"❌ 틀린 문제 다시 보기 ({len(wrong)}개)"):
            for n, q in wrong:
                st.markdown(f"**Q{n + 1}. {q['q']}** → 정답 **{q['a']}**")
                st.caption(q["exp"])

    st.markdown("#### 📢 친구에게 자랑하기")
    st.code(f"나는 캠코 생활금융 OX에서 '{r['emoji']} {r['name']}'가 나왔다! 너는 몇 점?", language=None)

    st.button("다시 하기 🔄", on_click=reset, width="stretch")

# ─────────────────────────────────────────
# 7. 안내 문구 (모든 화면 하단)
# ─────────────────────────────────────────
st.divider()
st.caption("이 퀴즈는 캠코(한국자산관리공사) 공개 자료를 바탕으로 개인이 만든 학습용 콘텐츠이며, "
           "캠코의 공식 서비스가 아닙니다. 정확한 기준과 신청 방법은 공식 홈페이지에서 확인하세요.")
