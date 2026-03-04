# Execution Plan — Duo AgentFlow Auditor

> 구현팀용 실행 계획서. Phase 단위로 관리하며, 각 태스크는 체크리스트로 추적.
> **예상 총 소요: 5일 (풀타임 기준)**

---

## Phase Overview

| Phase | 이름 | 목표 | 소요 | 선행 조건 |
|-------|------|------|------|----------|
| **0** | 환경 준비 | GitLab 샌드박스 접근 + 프로젝트 생성 | 0.5일 | 없음 |
| **1** | 코어 에이전트 | Scanner + Reporter 동작 검증 | 1.5일 | Phase 0 |
| **2** | 플로우 연결 | 2-에이전트 플로우 트리거→액션 검증 | 1일 | Phase 1 |
| **3** | 확장 에이전트 | Fixer + Metrics 추가, 4-에이전트 체인 | 1일 | Phase 2 |
| **4** | "와" 순간 + 폴리시 | 시각적 리포트, Before/After, 차별화 요소 | 0.5일 | Phase 3 |
| **5** | 데모 + 제출 | 영상 녹화, Devpost 제출, 최종 검증 | 0.5일 | Phase 4 |

---

## Phase 0 — 환경 준비 (0.5일)

### 목표
GitLab 해커톤 샌드박스에서 프로젝트가 동작하는 상태를 만든다.

### 태스크

- [ ] **0-1** 해커톤 그룹 접근 요청
  - https://forms.gle/EeCH2WWUewK3eGmVA 에서 접근 요청
  - 승인될 때까지 대기 (보통 24시간 이내)
  - ⚠️ **블로커**: 이거 없으면 아무것도 못 함. 최우선 처리

- [ ] **0-2** GitLab 프로젝트 생성
  - https://gitlab.com/gitlab-ai-hackathon 에서 New project
  - 이름: `duo-agentflow-auditor`
  - Visibility: **Public**
  - Initialize with README 체크

- [ ] **0-3** GitHub → GitLab 미러링
  - 📖 **상세 절차**: [`docs/GITLAB_MIRROR_GUIDE.md`](GITLAB_MIRROR_GUIDE.md) 참조
  - 권장: **방법 A (수동 Push)** — 가장 단순하고 확실
  ```bash
  git clone https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
  cd duo-agentflow-auditor
  git remote add gitlab https://gitlab.com/gitlab-ai-hackathon/{namespace}/duo-agentflow-auditor.git
  git push gitlab main
  ```
  - ⚠️ GitLab 프로젝트 생성 시 **README 초기화 해제** 필수 (충돌 방지)

- [ ] **0-4** GitLab Duo 기능 활성화 확인
  - Settings → General → Visibility → GitLab Duo features 활성화
  - Automate 메뉴가 보이는지 확인 (Agents, Flows, Triggers, Sessions)

- [ ] **0-5** MIT License 표시 확인
  - 프로젝트 메인 페이지 상단에 "MIT License" 뱃지 표시되는지 확인
  - 안 보이면: Settings → General → Project → License 설정

### Phase 0 완료 조건
✅ GitLab 프로젝트 URL 접근 가능 + Automate 메뉴 표시 + 코드 push 완료

---

## Phase 1 — 코어 에이전트 (1.5일)

### 목표
Scanner와 Reporter 에이전트가 개별적으로 정상 동작하는 것을 확인한다.

### 태스크

#### 1A: Scanner 에이전트 생성 + 테스트 (0.5일)

- [ ] **1A-1** Scanner 에이전트 생성
  - Automate → Agents → New agent
  - `agents/scanner.md`에서 설정값 + 시스템 프롬프트 복붙
  - 도구 8개 선택: List Merge Request Diffs, Read File, Read Files, Get Repository File, Grep, Find Files, List Dir, Get Merge Request
  - Visibility: Public → Create agent

- [ ] **1A-2** Scanner 에이전트 활성화
  - Managed 탭 → Scanner 선택 → Enable
  - Group + Project 선택 → Enable

- [ ] **1A-3** Scanner 단독 테스트 (Chat)
  - GitLab Duo Chat 열기 → Scanner 에이전트 선택
  - 테스트 프롬프트: "Analyze the file examples/vulnerable-mr/unsafe_script.py for security risks"
  - **검증**: JSON 형태의 findings가 반환되는지 확인
  - **검증**: risk_score, severity, category 필드가 올바른지 확인

- [ ] **1A-4** Scanner 프롬프트 튜닝 (필요시)
  - 출력이 기대와 다르면 시스템 프롬프트 수정
  - 특히: JSON 출력 포맷이 일관적인지, 위양성 없는지 확인
  - 📝 **문서 업데이트**: 수정된 프롬프트를 `agents/scanner.md`에 반영

#### 1B: Reporter 에이전트 생성 + 테스트 (0.5일)

- [ ] **1B-1** Reporter 에이전트 생성
  - `agents/reporter.md`에서 설정값 + 시스템 프롬프트 복붙
  - 도구 6개 선택: Create Merge Request Note, Create Issue, Create Issue Note, Update Issue, Get Merge Request, Gitlab Issue Search

- [ ] **1B-2** Reporter 에이전트 활성화

- [ ] **1B-3** Reporter 단독 테스트 (Chat)
  - Scanner 결과를 복사해서 Reporter에게 전달
  - 테스트 프롬프트: "Generate a security report for this MR based on these findings: {Scanner JSON}"
  - **검증**: 마크다운 리포트가 설계대로 생성되는지
  - **검증**: 리스크 테이블, 이모지, 심각도 뱃지 올바른지

- [ ] **1B-4** Reporter MR 코멘트 테스트
  - 실제 MR에서 Reporter에게 코멘트 요청
  - **검증**: MR 코멘트가 실제로 생성되는지 (create_merge_request_note 도구)
  - **검증**: DANGER 등급일 때 이슈가 생성되는지 (create_issue 도구)
  - 🎯 **"와" 체크포인트**: MR 코멘트가 예쁘게 나오면 스크린샷 캡처

#### 1C: 탐지 정확도 검증 (0.5일)

- [ ] **1C-1** 취약 파일 스캔 결과 검증
  - `examples/vulnerable-mr/unsafe_script.py` → 최소 8개 finding 기대
  - `examples/vulnerable-mr/risky_config.yaml` → 최소 6개 finding 기대
  - `examples/vulnerable-mr/insecure_fetch.js` → 최소 6개 finding 기대

- [ ] **1C-2** 안전 파일 스캔 결과 검증
  - `examples/safe-mr/safe_script.py` → 0개 finding 기대
  - `examples/safe-mr/safe_config.yaml` → 0개 finding 기대

- [ ] **1C-3** 위양성/위음성 목록 작성
  - 놓치는 패턴 → 시스템 프롬프트에 명시적으로 추가
  - 오탐 패턴 → 프롬프트에 제외 조건 추가
  - 📝 **문서 업데이트**: `rules/*.json`에 반영

### Phase 1 완료 조건
✅ Scanner가 취약 파일에서 8+ findings 반환 + Reporter가 MR 코멘트 생성 + 안전 파일에서 0 findings

---

## Phase 2 — 플로우 연결 (1일)

### 목표
Scanner → Reporter 2-에이전트 플로우가 트리거로 자동 실행된다.

### 태스크

#### 2A: 플로우 생성 (0.25일)

- [ ] **2A-1** 2-에이전트 축소 플로우 YAML 작성
  - `flows/security-audit.yml`에서 fix_agent, metrics_agent 주석 처리
  - scan_agent → report_agent → end 만 남기기
  - ⚠️ **핵심**: 전체 4-에이전트를 한번에 시도하지 말고, 2개부터 검증

- [ ] **2A-2** 플로우 생성 (UI)
  - Automate → Flows → New flow
  - 축소된 YAML 붙여넣기
  - ⚠️ YAML 문법 오류 시 에러 메시지 확인 → 수정

- [ ] **2A-3** 플로우 활성화 + 트리거 설정
  - Enable → Group + Project 선택
  - 트리거: ✅ Mention, ✅ Assign reviewer
  - 서비스 계정 이름 확인: `ai-security-audit-flow-{group}`

#### 2B: 트리거 → 액션 검증 (0.5일)

- [ ] **2B-1** 테스트 MR 생성
  ```bash
  git checkout -b test/phase2-trigger-test
  cp examples/vulnerable-mr/unsafe_script.py test_vuln.py
  git add test_vuln.py
  git commit -m "test: trigger test with vulnerable code"
  git push origin test/phase2-trigger-test
  ```
  - GitLab UI에서 MR 생성 (test/phase2-trigger-test → main)

- [ ] **2B-2** 트리거 실행
  - MR 코멘트에 `@ai-security-audit-flow-{group} please review this MR` 입력
  - **관찰**: Automate → Sessions에서 플로우 시작 확인

- [ ] **2B-3** 결과 검증
  - **검증 1**: 플로우 세션이 "running" → "completed" 전환
  - **검증 2**: MR에 보안 리포트 코멘트 생성
  - **검증 3**: DANGER 등급이면 이슈 생성
  - ⏱️ **타이밍 측정**: 트리거부터 코멘트까지 소요 시간 기록 (데모 계획용)

- [ ] **2B-4** 안전 코드 MR 테스트
  - safe-mr 파일로 MR 생성 → 트리거 → SAFE 등급 확인
  - 🎯 **"와" 체크포인트**: DANGER vs SAFE 결과 대비 스크린샷 캡처

#### 2C: 디버깅 (0.25일 예비)

- [ ] **2C-1** 플로우 실패 시 디버깅
  - Automate → Sessions에서 실패 로그 확인
  - 흔한 문제:
    - 도구 권한 미설정 → 에이전트 편집에서 도구 재선택
    - 프롬프트 출력 형식 불일치 → 시스템 프롬프트 수정
    - 타임아웃 → 스캔 범위 축소 (AGENTS.md exclude 추가)
  - 📝 **문서 업데이트**: 발생한 이슈와 해결법을 `docs/SETUP_GUIDE.md` 트러블슈팅에 추가

### Phase 2 완료 조건
✅ @mention으로 트리거 → Scanner 실행 → Reporter가 MR 코멘트 자동 생성 (end-to-end)

---

## Phase 3 — 확장 에이전트 (1일)

### 목표
Fixer + Metrics 에이전트를 추가하여 4-에이전트 전체 체인을 완성한다.

### 태스크

#### 3A: Fixer 에이전트 (0.5일)

- [ ] **3A-1** Fixer 에이전트 생성 + 활성화
  - `agents/fixer.md`에서 설정 복붙
  - 도구 8개 선택

- [ ] **3A-2** Fixer 단독 테스트 (Chat)
  - Scanner 결과를 수동으로 전달
  - "Fix the shell=True finding in test_vuln.py line 13"
  - **검증**: 코드 수정이 올바른지, 커밋이 생성되는지

- [ ] **3A-3** Fixer 플로우 통합
  - YAML에서 fix_agent 주석 해제
  - 라우터: report_agent → fix_agent → end
  - 플로우 수정 후 재테스트

- [ ] **3A-4** Fix MR 자동 생성 검증
  - 트리거 실행 후 `agentflow-fix/{mr_iid}` 브랜치 생성 확인
  - Fix MR이 원본 MR을 참조하는지 확인
  - 🎯 **"와" 체크포인트**: 자동 생성된 Fix MR 스크린샷 캡처

#### 3B: Metrics 에이전트 (0.3일)

- [ ] **3B-1** Metrics 에이전트 생성 + 활성화
  - `agents/metrics.md`에서 설정 복붙
  - 도구 6개 선택

- [ ] **3B-2** Metrics 단독 테스트 (Chat)
  - Scanner 결과를 전달하고 베이스라인 생성 요청
  - **검증**: `.agentflow-auditor/baseline.json` 생성 확인
  - **검증**: 지속가능성 메트릭 (토큰, 에너지, 탄소) 출력 확인

- [ ] **3B-3** Metrics 플로우 통합
  - YAML에서 metrics_agent 주석 해제
  - 전체 라우터: scan → report → fix → metrics → end
  - 📝 **문서 업데이트**: 최종 동작하는 YAML을 `flows/security-audit.yml`에 반영

#### 3C: 전체 체인 검증 (0.2일)

- [ ] **3C-1** 4-에이전트 전체 플로우 실행
  - 새 MR → 트리거 → 4개 에이전트 순차 실행 확인
  - ⏱️ **타이밍**: 전체 플로우 소요 시간 기록 (3분 미만이어야 데모 가능)

- [ ] **3C-2** 타임아웃 대응 (필요시)
  - 전체 플로우가 5분 초과 시:
    - **옵션 A**: Metrics를 OneOffComponent로 변경 (이미 설정됨)
    - **옵션 B**: Fix + Metrics를 병렬 실행 (라우터 분기)
    - **옵션 C**: Metrics를 플로우에서 제외, 별도 에이전트로 Chat에서 수동 실행

- [ ] **3C-3** 2회차 실행 (베이스라인 델타 확인)
  - 첫 번째 실행 후 다시 트리거
  - **검증**: 베이스라인 델타가 정확히 계산되는지
  - 🎯 **"와" 체크포인트**: "Previous: 8 findings → Current: 3 findings → Δ-5" 스크린샷

### Phase 3 완료 조건
✅ 4-에이전트 전체 플로우 트리거→완료 + Fix MR 자동 생성 + 베이스라인 델타 표시

---

## Phase 4 — "와" 순간 + 폴리시 (0.5일)

### 목표
심사위원이 "이건 다르다"라고 느끼는 시각적 임팩트를 만든다.

### 태스크

- [ ] **4-1** MR 코멘트 시각적 완성도 확인
  - Reporter 프롬프트를 조정하여:
    - 이모지 뱃지가 올바르게 표시되는지 (🚨, ⚠️, ✅)
    - 테이블이 깨지지 않는지
    - `<details>` 접기가 동작하는지
  - 📸 **스크린샷 3장** 캡처: DANGER 리포트, SAFE 리포트, 델타 리포트

- [ ] **4-2** Before/After 데모 자료 준비
  - "Before" 스크린샷: MR이 리뷰 대기 중 (빨간 경고 없음)
  - "After" 스크린샷: 에이전트 리포트 + Fix MR + 이슈 자동 생성
  - README.md에 스크린샷 삽입

- [ ] **4-3** "와" 순간 강화 요소 구현 (아래 WOW_MOMENTS.md 참조)
  - 우선순위 1: 리스크 히트맵 (파일별 색상)
  - 우선순위 2: Fix MR diff 하이라이트
  - 우선순위 3: Green 메트릭 시각화

- [ ] **4-4** README.md 최종 업데이트
  - 실제 스크린샷 삽입
  - 실제 동작 확인된 내용으로 수정
  - 설치/사용법이 정확한지 재검증

- [ ] **4-5** AGENTS.md 최종 튜닝
  - 실테스트에서 발견된 위양성 도메인 추가
  - 불필요한 경고를 줄이는 제외 경로 추가

### Phase 4 완료 조건
✅ 스크린샷 3장 확보 + Before/After 대비 자료 + README 업데이트

---

## Phase 5 — 데모 + 제출 (0.5일)

### 목표
3분 데모 영상 녹화 + Devpost 제출 완료.

### 태스크

#### 5A: 데모 준비 (0.2일)

- [ ] **5A-1** 데모 환경 사전 준비
  - 브라우저: 깨끗한 GitLab 탭 (다른 탭 없음)
  - MR: 미리 생성해둔 취약 코드 MR (트리거 대기 상태)
  - 두 번째 MR: 수정 후 재실행용 (Safe 결과 보여줄 것)
  - 터미널: `git push` 명령어 미리 입력해놓기

- [ ] **5A-2** 데모 리허설 3회
  - 타이머로 3분 맞추기
  - 각 리허설 후 개선점 기록
  - 특히: 에이전트 응답 대기 시간 동안 설명할 내용 준비

- [ ] **5A-3** 사전 녹화 (안전망)
  - 최소 1회 성공적인 녹화를 미리 해놓기
  - 라이브 데모 실패 시 편집 소스로 사용

#### 5B: 영상 녹화 (0.2일)

- [ ] **5B-1** 영상 녹화
  - 도구: OBS Studio 또는 Loom (무료)
  - 해상도: 1920x1080
  - 오디오: 외장 마이크 권장 (내장 마이크도 OK)
  - 구조: `IMPLEMENTATION.md` §8 데모 스크립트 참조
  - ⚠️ **3분 초과 금지** — 심사위원은 3분 이후 안 봄

- [ ] **5B-2** 영상 편집 (필수 아님, 권장)
  - 에이전트 대기 시간 → 타임랩스 처리 (x4 속도 + "Processing..." 텍스트)
  - 핵심 결과 나올 때 → 확대 줌
  - 배경 음악: 저작권 없는 것만 (또는 없이)

- [ ] **5B-3** 영상 업로드
  - YouTube에 **Public**으로 업로드
  - 제목: "Duo AgentFlow Auditor — GitLab AI Hackathon Demo"
  - 설명에 프로젝트 URL 포함

#### 5C: Devpost 제출 (0.1일)

- [ ] **5C-1** Devpost 제출 폼 작성
  - `docs/DEVPOST_SUBMISSION.md` 내용 복붙
  - GitLab 프로젝트 URL 입력
  - YouTube 영상 URL 입력
  - Built With 태그: GitLab Duo Agent Platform, Anthropic Claude, CI/CD

- [ ] **5C-2** 최종 체크리스트 (제출 전)
  - [ ] GitLab 프로젝트가 Public인가?
  - [ ] MIT License가 프로젝트 페이지에 표시되는가?
  - [ ] README.md에 기능 설명 + 설치법이 있는가?
  - [ ] 데모 영상이 3분 이하인가?
  - [ ] 영상에서 트리거→액션이 명확히 보이는가?
  - [ ] 영상이 Public 접근 가능한가?
  - [ ] 소스 코드에 저작권 침해 없는가?

- [ ] **5C-3** 제출 버튼 클릭
  - 마감: **March 25, 2026 @ 2:00pm EDT** (한국시간 March 26 새벽 3:00)
  - ⚠️ **마감 24시간 전 제출 권장** — 마지막 날 서버 과부하 가능

### Phase 5 완료 조건
✅ YouTube 영상 업로드 + Devpost 제출 완료 + 모든 체크리스트 통과

---

## 위험 관리 매트릭스

| 위험 | 확률 | 영향 | 대응 | 담당 Phase |
|------|------|------|------|-----------|
| 해커톤 그룹 접근 지연 | 중 | 🚨 치명 | 접근 요청 최우선 처리, Discord에 문의 | Phase 0 |
| 플로우 YAML 파싱 오류 | 높 | ⚠️ 높 | 2-에이전트로 축소 테스트 → 점진 확장 | Phase 2 |
| 에이전트 도구 권한 오류 | 중 | ⚠️ 높 | 도구 하나씩 추가하며 검증 | Phase 1 |
| 4-에이전트 체인 타임아웃 | 중 | ⚠️ 높 | 3가지 대안 준비 (3C-2 참조) | Phase 3 |
| Fix MR 생성 실패 | 중 | ⚠️ 보통 | Fixer를 Chat-only로 전환, 플로우에서 제거 | Phase 3 |
| 데모 중 라이브 실패 | 낮 | 🚨 치명 | 사전 녹화 백업 영상 준비 (5A-3) | Phase 5 |
| Devpost 서버 과부하 | 낮 | ⚠️ 높 | 마감 24시간 전 제출 | Phase 5 |

---

## 일일 마일스톤 체크

| Day | 완료 상태 | 검증 방법 |
|-----|----------|----------|
| Day 1 | Phase 0 + Phase 1A 완료 | Scanner가 Chat에서 findings 반환 |
| Day 2 | Phase 1 완료 | Scanner + Reporter 각각 동작 확인 |
| Day 3 | Phase 2 완료 | @mention → MR 코멘트 자동 생성 (end-to-end) |
| Day 4 | Phase 3 완료 | 4-에이전트 전체 체인 동작 |
| Day 5 | Phase 4 + 5 완료 | 영상 업로드 + Devpost 제출 |

---

## Fallback 전략 (최악의 경우)

만약 **커스텀 플로우 YAML이 동작하지 않을 경우**:

### Plan B: 단일 에이전트 + CI/CD

1. Scanner + Reporter 기능을 하나의 커스텀 에이전트로 통합
2. `.gitlab-ci.yml`에 보안 스캔 Job 추가 (MR 이벤트 트리거)
3. CI Job에서 에이전트를 Chat API로 호출
4. 결과를 MR 코멘트로 POST (GitLab API)

이 경우에도 **트리거→액션** 요건은 충족하며, 데모 가능.

### Plan C: 외부 에이전트 (Claude Code)

1. `.gitlab/duo/flows/claude.yaml`로 외부 에이전트 설정
2. Claude Code를 컨테이너에서 실행
3. 기존 스캐닝 로직을 Claude의 프롬프트로 구현

검증된 외부 에이전트 YAML 예시가 `references/guides/yaml-config-complete-reference.md`에 있음.
