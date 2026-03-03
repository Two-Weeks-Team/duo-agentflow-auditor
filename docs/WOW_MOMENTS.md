# "와" 순간 설계 — Duo AgentFlow Auditor

> 심사위원이 "이건 다르다"라고 느끼는 시각적 임팩트와 차별화 요소 설계.
> Phase 4 (태스크 4-3) 구현 시 이 문서를 참조하여 우선순위대로 적용한다.

---

## 목차

1. [Before/After 극적 대비](#1-beforeafter-극적-대비)
2. [리스크 히트맵 — 파일별 색상 코드](#2-리스크-히트맵--파일별-색상-코드)
3. [Fix MR Diff 하이라이트](#3-fix-mr-diff-하이라이트)
4. [Green 메트릭 시각화](#4-green-메트릭-시각화)
5. [베이스라인 트렌드 차트](#5-베이스라인-트렌드-차트)
6. [데모 영상 "Magic Moment" 연출](#6-데모-영상-magic-moment-연출)
7. [구현 우선순위 및 체크리스트](#7-구현-우선순위-및-체크리스트)

---

## 1. Before/After 극적 대비

### 핵심 메시지

> 심사위원은 "문제가 얼마나 심각한지"와 "해결이 얼마나 빠른지"의 **대비**에서 감동한다.

### Before 시나리오 (수동 리뷰)

```
┌─────────────────────────────────────────────────────┐
│  MR #42: "Add data pipeline script"                 │
│                                                     │
│  Status: ⏳ Awaiting review                         │
│  Reviewers: @senior-dev (busy, 2일 대기 중)          │
│  Comments: 0                                        │
│  Security scan: ❌ None configured                  │
│                                                     │
│  ┌── unsafe_script.py ──────────────────────────┐   │
│  │  13: subprocess.run(cmd, shell=True)          │   │
│  │  27: eval(user_input)                         │   │
│  │  41: requests.get(f"http://{host}/api")       │   │
│  │  55: os.system(f"rm -rf {path}")              │   │
│  └───────────────────────────────────────────────┘   │
│                                                     │
│  💤 2일 후... 리뷰어가 13번 줄만 발견. 나머지 놓침.   │
│  ✅ Merged. 프로덕션 인시던트 발생. 🔥               │
└─────────────────────────────────────────────────────┘
```

**캡처 포인트**: MR 페이지에서 "Awaiting review" 상태, 댓글 0개, 보안 스캔 없음.

### After 시나리오 (AgentFlow Auditor)

```
┌─────────────────────────────────────────────────────┐
│  MR #42: "Add data pipeline script"                 │
│                                                     │
│  Status: ⏳ Awaiting review                         │
│  Reviewers: @duo-agentflow-auditor (assigned)       │
│  Comments: 1 (Security Report)                      │
│  ⏱️ 응답 시간: 45초                                 │
│                                                     │
│  ┌── 🛡️ AgentFlow Auditor — Security Report ────┐  │
│  │                                                │  │
│  │  Grade: 🚨 DANGER                             │  │
│  │  Recommendation: FAIL — do not merge           │  │
│  │                                                │  │
│  │  ┌─ Risk Summary ──────────────────────┐      │  │
│  │  │ Total Findings:    8                │      │  │
│  │  │ Actionable:        6                │      │  │
│  │  │ Max Risk:          95               │      │  │
│  │  │ High Risk (≥70):   4                │      │  │
│  │  └─────────────────────────────────────┘      │  │
│  │                                                │  │
│  │  🚨 unsafe_script.py:55 — rm -rf (95/100)     │  │
│  │  🚨 unsafe_script.py:13 — shell=True (88/100) │  │
│  │  🚨 unsafe_script.py:27 — eval() (85/100)     │  │
│  │  ⚠️ unsafe_script.py:41 — HTTP (62/100)       │  │
│  │                                                │  │
│  │  📝 Issue Created: #127 "Security Audit"       │  │
│  │  🔧 Fix MR: !43 (auto-generated patches)      │  │
│  │  🌱 Energy: 0.012 kWh | CO₂: 0.005 kg        │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**캡처 포인트**: MR 페이지에서 자동 생성된 리포트 코멘트, 이슈, Fix MR 전부 한 화면에.

### 스크린샷 구성 (README용)

| 순서 | 내용 | 파일명 | 비고 |
|------|------|--------|------|
| 1 | Before: 빈 MR (리뷰 없음) | `screenshots/before-no-review.png` | 가장 먼저 캡처 |
| 2 | After: DANGER 리포트 | `screenshots/after-danger-report.png` | 리포트 코멘트 전체 |
| 3 | After: 자동 생성된 Fix MR | `screenshots/after-fix-mr.png` | diff 포함 |
| 4 | After: 자동 생성된 Issue | `screenshots/after-issue-created.png` | 라벨 포함 |

---

## 2. 리스크 히트맵 — 파일별 색상 코드

### 설계

MR 코멘트 안에 **파일별 리스크를 한눈에** 보여주는 시각적 요소.
GitLab Markdown에서 이모지 + 유니코드 블록으로 히트맵을 구현한다.

### MR 코멘트 내 구현 예시

```markdown
### 🗺️ Risk Heatmap

| Risk | File | Findings | Max Score |
|------|------|----------|-----------|
| 🟥🟥🟥🟥🟥 | `unsafe_script.py` | 5 | 95 |
| 🟥🟥🟥🟧⬜ | `risky_config.yaml` | 3 | 78 |
| 🟧🟧⬜⬜⬜ | `insecure_fetch.js` | 2 | 62 |
| 🟩🟩🟩🟩🟩 | `safe_script.py` | 0 | 0 |
| 🟩🟩🟩🟩🟩 | `safe_config.yaml` | 0 | 0 |
```

### 색상 코드 규칙

| 이모지 | Risk Range | 의미 |
|--------|-----------|------|
| 🟥 | 70-100 | High risk (danger) |
| 🟧 | 40-69 | Medium risk (warning) |
| 🟨 | 20-39 | Low risk (info) |
| 🟩 | 0-19 | Safe / No findings |
| ⬜ | — | Padding (미사용 슬롯) |

### 바 길이 계산

```
bar_length = 5 (고정)
filled = ceil(max_risk_score / 20)
color = 🟥 if max_risk >= 70, 🟧 if >= 40, 🟨 if >= 20, 🟩 otherwise
bar = color × filled + ⬜ × (5 - filled)
```

### Reporter 프롬프트에 추가할 지시

```
After the Risk Summary table and before Top Findings, include a Risk Heatmap section:
- List each scanned file in descending order of max risk score
- Show a 5-block color bar using emoji: 🟥 (70+), 🟧 (40-69), 🟨 (20-39), 🟩 (0-19)
- Fill blocks based on max_risk_score / 20, rounded up
- Pad remaining blocks with ⬜
- Include columns: Risk (bar), File, Findings count, Max Score
```

### 기대 효과

- **한 눈에**: 어떤 파일이 위험한지 스크롤 없이 파악
- **시각적 대비**: 빨간색 파일과 초록색 파일의 극적 대비가 심사위원 눈을 끔
- **GitLab 네이티브**: 외부 이미지 없이 마크다운만으로 구현 — 어디서든 렌더링

---

## 3. Fix MR Diff 하이라이트

### 설계

Fix Agent가 자동 생성한 패치가 **원본 코드 vs 수정 코드**로 명확히 보이도록 구성한다.
MR 코멘트 내에 before/after를 인라인으로 보여주고, 실제 Fix MR의 diff 링크를 제공한다.

### MR 코멘트 내 구현 예시

```markdown
### 🔧 Auto-Fix Preview

<details>
<summary>🔧 Fix 1/3: <code>unsafe_script.py:13</code> — shell=True → subprocess list</summary>

**Before:**
```python
subprocess.run(cmd, shell=True)
```

**After:**
```python
subprocess.run(shlex.split(cmd), shell=False)
```

**Why:** `shell=True` allows shell injection via metacharacters. Using `shlex.split()` safely tokenizes the command while keeping `shell=False`.

</details>

<details>
<summary>🔧 Fix 2/3: <code>unsafe_script.py:27</code> — eval() → ast.literal_eval()</summary>

**Before:**
```python
result = eval(user_input)
```

**After:**
```python
import ast
result = ast.literal_eval(user_input)
```

**Why:** `eval()` executes arbitrary code. `ast.literal_eval()` safely parses Python literals only.

</details>

<details>
<summary>🔧 Fix 3/3: <code>unsafe_script.py:41</code> — HTTP → HTTPS</summary>

**Before:**
```python
requests.get(f"http://{host}/api/data")
```

**After:**
```python
requests.get(f"https://{host}/api/data")
```

**Why:** HTTP transmits data in plaintext. HTTPS encrypts the connection.

</details>

🔗 **Full Fix MR**: [!43 — security-fix/42](link) (3 files changed, 6 insertions, 3 deletions)
```

### Fixer 프롬프트에 추가할 지시

```
When creating fixes, also output a summary for the Reporter to include in the MR comment:
- For each fix: file:line, pattern name, before snippet, after snippet, explanation
- Format as collapsible <details> sections
- Number fixes: "Fix 1/N", "Fix 2/N", etc.
- Include a link to the created Fix MR at the bottom
```

### 기대 효과

- **즉각적 이해**: 심사위원이 diff를 보지 않아도 무엇이 바뀌었는지 파악
- **교육적**: 왜 바꿨는지 설명이 포함되어 개발자 학습 효과
- **원클릭**: Fix MR 링크를 클릭하면 전체 diff로 이동

---

## 4. Green 메트릭 시각화

### 설계

Green Agent(Metrics Agent) 상 노리기 위한 시각적 지속가능성 리포트.
에너지 소비와 탄소 발자국을 **체감할 수 있는 비유**로 표현한다.

### MR 코멘트 내 구현 예시

```markdown
### 🌱 Sustainability Report

| Metric | Value |
|--------|-------|
| Tokens Used | 12,450 |
| Energy | 0.0037 kWh |
| CO₂ Footprint | 0.0014 kg |
| Efficiency | 2.4 findings / 1K tokens |

#### Impact Comparison

| This Scan | Equivalent To |
|-----------|---------------|
| 0.0037 kWh | 💡 LED bulb for 13 seconds |
| 0.0014 kg CO₂ | 🚗 Car driving 5.6 meters |

#### Optimization Applied
- ✅ Scanned only changed files (saved ~60% tokens)
- ✅ Skipped binary files and vendor directories
- 💡 Suggestion: Add `.agentflow-auditor/exclude` for test fixtures

#### Cumulative Impact (3 scans)
| Metric | Total | Per Scan Avg |
|--------|-------|-------------|
| Scans | 3 | — |
| Tokens | 34,200 | 11,400 |
| Energy | 0.0103 kWh | 0.0034 kWh |
| CO₂ | 0.0040 kg | 0.0013 kg |
| 📉 Trend | -12% energy per scan | Improving |
```

### 비유 테이블 (Metrics 프롬프트에 포함)

```
Energy equivalences (include the closest match):
- 0.001 kWh = 💡 LED bulb for 3.6 seconds
- 0.01 kWh  = 💡 LED bulb for 36 seconds
- 0.1 kWh   = 📱 Charging a phone to 10%
- 1.0 kWh   = 🖥️ Running a laptop for 2 hours

Carbon equivalences:
- 0.001 kg CO₂ = 🚗 Car driving 4 meters
- 0.01 kg CO₂  = 🚗 Car driving 40 meters
- 0.1 kg CO₂   = 🚗 Car driving 400 meters
- 1.0 kg CO₂   = 🌳 One tree absorbs this in ~1 hour
```

### Metrics 프롬프트에 추가할 지시

```
In the Sustainability Report section:
1. Always include the Impact Comparison table with real-world analogies
2. Pick the closest equivalence from the provided table
3. If cumulative data exists (3+ scans), show the Cumulative Impact table
4. Include a trend indicator: 📈 (getting worse) or 📉 (improving) or ➡️ (stable)
5. List optimization suggestions specific to the scanned repository
```

### 기대 효과

- **체감 가능**: 추상적인 kWh를 "LED 13초", "차 5.6m"로 변환 — 심사위원이 즉시 이해
- **차별화**: 다른 해커톤 제출물 중 이런 수준의 Green 시각화를 하는 프로젝트는 거의 없음
- **누적 추적**: 반복 사용할수록 가치가 드러남 — "3번 스캔으로 에너지 12% 절감" 등

---

## 5. 베이스라인 트렌드 차트

### 설계

스캔 히스토리가 쌓이면 **ASCII 기반 트렌드 차트**로 보안 수준의 변화를 보여준다.
GitLab Markdown에서 외부 이미지 없이 구현 가능한 방법을 사용한다.

### MR 코멘트 내 구현 예시 (3+ 스캔 시)

```markdown
### 📈 Security Trend (last 5 scans)

```
Risk Score
100 ┤
 90 ┤                     
 80 ┤  ●                  
 70 ┤  │                  
 60 ┤  │         ●        
 50 ┤  │         │        
 40 ┤  │    ●    │   ●    
 30 ┤  │    │    │   │    
 20 ┤  │    │    │   │  ● 
 10 ┤  │    │    │   │  │ 
  0 ┼──┴────┴────┴───┴──┴──
     MR#38 MR#39 MR#41 MR#42 MR#43
     DANGER WARN  WARN  WARN  SAFE
```

📉 **Trend: Improving** — Average risk decreased 72% over 5 scans
🏆 **Fix adoption**: 85% of suggested fixes were applied
```

### 간소 버전 (2 스캔 시)

```markdown
### 📊 Baseline Delta

| | Previous (MR#41) | Current (MR#42) | Δ |
|---|---|---|---|
| Findings | 8 | 3 | **-5** 📉 |
| Actionable | 6 | 2 | **-4** 📉 |
| Max Risk | 88 | 62 | **-26** 📉 |
| Grade | 🚨 DANGER | ⚠️ WARNING | Improved ✅ |
```

### Metrics 프롬프트에 추가할 지시

```
If history.jsonl has 2 entries: show a simple Baseline Delta table
If history.jsonl has 3+ entries: show an ASCII trend chart
- X-axis: MR IIDs (last 5)
- Y-axis: Max risk score (0-100)
- Data points: ● at the risk level
- Below each: grade badge
- Include trend line description and fix adoption rate
```

### 기대 효과

- **서사**: 단일 스캔이 아니라 **보안 개선 여정**을 보여줌
- **반복 가치**: "이 도구를 계속 쓰면 보안이 좋아진다"는 증거
- **데모 연출**: 영상에서 첫 스캔(DANGER) → 수정 후 재스캔(SAFE) 대비가 극적

---

## 6. 데모 영상 "Magic Moment" 연출

### 타임라인 (3분 = 180초)

```
시간      내용                                "와" 요소
──────────────────────────────────────────────────────────────
0:00-0:15  Hook + 문제 제시                    
           "AI가 코드를 빠르게 생성하지만,
            보안 리뷰가 병목입니다."

0:15-0:30  Before 화면                         ❌ 빈 MR, 리뷰 없음
           MR #42 열기 → 아무 코멘트 없음
           "이 MR에는 4개의 보안 취약점이
            숨어있지만, 아무도 모릅니다."

0:30-0:45  트리거                              ⚡ 타이핑 순간
           @duo-agentflow-auditor 입력
           Enter 누르는 순간 → 잠깐 멈춤
           "하나의 멘션으로 4개 에이전트가
            동시에 작동합니다."

0:45-1:15  에이전트 동작 중                     🔄 실시간 진행
           Automate → Sessions 페이지 보여주기
           Scanner → Reporter → Fixer → Metrics
           각 에이전트 상태 전환 보여주기
           (대기 시간은 x4 타임랩스)

────────── ★ MAGIC MOMENT 1 ──────────────────────────────────
1:15-1:45  리포트 등장                          🎯 핵심 임팩트
           MR 페이지로 돌아감
           코멘트 새로고침 → 리포트 등장!
           🚨 DANGER 뱃지, 리스크 히트맵
           "45초 만에 전체 보안 리포트가
            MR에 자동으로 게시되었습니다."

           줌인: 히트맵 + Top Findings 테이블
           줌인: Fix 제안 (collapsible 열기)

────────── ★ MAGIC MOMENT 2 ──────────────────────────────────
1:45-2:00  Fix MR 자동 생성                     🔧 자동 수정
           MR 목록으로 이동 → !43 Fix MR 클릭
           diff 보여주기: shell=True → split()
           "수정 코드까지 자동으로 생성해서
            새 MR로 제출합니다."

────────── ★ MAGIC MOMENT 3 ──────────────────────────────────
2:00-2:15  이슈 자동 생성                       📋 워크플로우 자동화
           Issues 페이지 → "🚨 Security Audit"
           라벨: security-risk, agentflow-auditor
           "DANGER 등급이면 자동으로 추적 이슈를
            생성합니다."

────────── ★ MAGIC MOMENT 4 ──────────────────────────────────
2:15-2:35  재스캔 (After Fix)                   📉 극적 변화
           Fix MR 머지 후 재스캔 트리거
           (사전 녹화된 결과 보여주기)
           🚨 DANGER → ✅ SAFE
           베이스라인 델타: "Findings: 8→0, -100%"
           트렌드 차트 보여주기
           "수정 후 재스캔하면 보안 개선을
            수치로 증명합니다."

────────── ★ MAGIC MOMENT 5 ──────────────────────────────────
2:35-2:50  Green 메트릭                         🌱 차별화
           지속가능성 리포트 줌인
           "이 모든 스캔에 LED 전구 13초 분량의
            에너지만 사용했습니다."
           탄소 발자국: "자동차 5.6미터 주행"

2:50-3:00  마무리                               💪 임팩트 정리
           "하나의 멘션. 네 개의 에이전트.
            제로 보안 사각지대.
            GitLab Duo Agent Platform 위에서."
──────────────────────────────────────────────────────────────
```

### Magic Moment 촬영 기법

| Moment | 연출 기법 | 시각적 효과 |
|--------|-----------|-------------|
| **#1 리포트 등장** | 페이지 새로고침 후 **3초 멈춤** → 스크롤 다운 | 심사위원이 리포트를 읽을 시간 확보 |
| **#2 Fix MR** | diff 화면에서 빨간줄(삭제)/초록줄(추가) 강조 | GitLab 네이티브 diff가 이미 시각적 |
| **#3 이슈 생성** | Issues 탭 클릭 → 이슈 제목+라벨 줌인 | 자동화의 완결성 증명 |
| **#4 Before→After** | 화면 분할 또는 빠른 전환 (DANGER → SAFE) | 가장 강력한 대비 효과 |
| **#5 Green** | 에너지 비유 텍스트 줌인 (LED 13초) | "이게 전부?"라는 놀라움 |

### 사전 준비 체크리스트

- [ ] MR #42 미리 생성 (취약 코드, 트리거 대기 상태)
- [ ] MR #43 사전 생성 (Fix MR 결과, 미리 머지된 상태)
- [ ] 재스캔 결과 SAFE 버전 미리 확보 (사전 녹화)
- [ ] 브라우저: 깨끗한 GitLab 탭만 (다른 탭 없음)
- [ ] 화면 녹화 도구 테스트 (OBS/Loom)
- [ ] 마이크 테스트 (내장 OK, 외장 권장)
- [ ] 타임랩스 편집 방법 확인 (에이전트 대기 시간용)

---

## 7. 구현 우선순위 및 체크리스트

### 우선순위 (P0 = 필수, P1 = 강력 권장, P2 = 있으면 좋음)

| Priority | "와" 요소 | 구현 난이도 | 임팩트 | 담당 |
|----------|-----------|------------|--------|------|
| **P0** | Before/After 스크린샷 | ⭐ 쉬움 | 🔥🔥🔥 | Phase 4 |
| **P0** | 리포트 등장 (Magic Moment #1) | ⭐ 쉬움 | 🔥🔥🔥 | Phase 2 완료 시 자동 |
| **P0** | DANGER → SAFE 대비 (Magic Moment #4) | ⭐⭐ 보통 | 🔥🔥🔥 | Phase 4 |
| **P1** | 리스크 히트맵 | ⭐⭐ 보통 | 🔥🔥 | Reporter 프롬프트 수정 |
| **P1** | Fix MR Diff (Magic Moment #2) | ⭐ 쉬움 | 🔥🔥 | Phase 3 완료 시 자동 |
| **P1** | Green 메트릭 비유 | ⭐⭐ 보통 | 🔥🔥 | Metrics 프롬프트 수정 |
| **P1** | 이슈 자동 생성 (Magic Moment #3) | ⭐ 쉬움 | 🔥🔥 | Phase 2 완료 시 자동 |
| **P2** | 베이스라인 트렌드 차트 | ⭐⭐⭐ 어려움 | 🔥 | Metrics 프롬프트 수정 |
| **P2** | 누적 Green 메트릭 | ⭐⭐ 보통 | 🔥 | 3+ 스캔 필요 |

### 프롬프트 수정 체크리스트

각 "와" 요소를 활성화하려면 에이전트 시스템 프롬프트에 지시를 추가해야 한다:

- [ ] **Reporter (`agents/reporter.md`)에 추가**:
  - [ ] Risk Heatmap 섹션 (§2의 프롬프트 추가 내용)
  - [ ] Auto-Fix Preview 섹션 (§3의 프롬프트 추가 내용, Fixer 결과 받아서 포함)

- [ ] **Fixer (`agents/fixer.md`)에 추가**:
  - [ ] Fix Summary 출력 (before/after/why per fix, Reporter에게 전달용)

- [ ] **Metrics (`agents/metrics.md`)에 추가**:
  - [ ] Impact Comparison 비유 테이블 (§4의 프롬프트 추가 내용)
  - [ ] ASCII 트렌드 차트 (§5의 프롬프트 추가 내용, 3+ 스캔 시)
  - [ ] 누적 임팩트 테이블 (§4의 Cumulative Impact)

### 스크린샷 캡처 체크리스트

| 순서 | 캡처 대상 | 용도 | 파일명 |
|------|-----------|------|--------|
| 1 | Before: 빈 MR 페이지 | README + 데모 | `before-empty-mr.png` |
| 2 | After: DANGER 리포트 (전체) | README + 데모 | `after-danger-full.png` |
| 3 | After: 리스크 히트맵 (줌인) | README | `after-heatmap.png` |
| 4 | After: Fix 제안 (열린 상태) | README | `after-fix-suggestions.png` |
| 5 | After: Fix MR diff | README + 데모 | `after-fix-mr-diff.png` |
| 6 | After: 자동 생성 이슈 | README | `after-issue-created.png` |
| 7 | After: SAFE 리포트 (재스캔) | README + 데모 | `after-safe-report.png` |
| 8 | After: 베이스라인 델타 | README + 데모 | `after-baseline-delta.png` |
| 9 | After: Green 메트릭 (줌인) | README | `after-green-metrics.png` |

---

## 부록: 심사위원 심리 분석

### 심사위원이 보는 시간

- **첫 30초**: README 훑기 → "이게 뭐 하는 거지?"
- **30초-2분**: 데모 영상 → "실제로 되는 건가?"
- **2-3분**: 코드/구조 확인 → "잘 만든 건가?"

### 각 시간대별 "와" 타겟

| 시간대 | 타겟 반응 | 우리의 무기 |
|--------|-----------|-------------|
| 첫 30초 | "와, 깔끔하네" | README 아키텍처 다이어그램 + 기능 테이블 |
| 30초-1분 | "오, 진짜 되네" | 트리거 입력 → 리포트 등장 (Magic Moment #1) |
| 1-2분 | "이건 좀 다르다" | Fix MR 자동 생성 + DANGER→SAFE 전환 |
| 2-3분 | "Green까지?" | 에너지 비유 + 트렌드 차트 |

### 경쟁 프로젝트 대비 차별점

| 다른 프로젝트 | 우리 프로젝트 |
|--------------|--------------|
| 단일 에이전트 Chat 데모 | 4-에이전트 자동 플로우 (트리거→액션) |
| 텍스트만 출력 | 시각적 히트맵 + 이모지 뱃지 + 테이블 |
| "가능합니다"로 끝남 | 실제 MR 코멘트 + 이슈 + Fix MR 생성 |
| 지속가능성 언급 없음 | Green 메트릭 + 에너지 비유 |
| 1회성 스캔 | 베이스라인 트래킹 + 트렌드 분석 |
