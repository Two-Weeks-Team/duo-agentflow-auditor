# GitLab Mirror Guide — GitHub → GitLab

> GitHub 레포(`Two-Weeks-Team/duo-agentflow-auditor`)를 GitLab 해커톤 그룹으로 미러링하는 전체 절차.
> 3가지 방법을 제공하며, 팀 상황에 맞게 선택한다.

---

## 목차

1. [사전 준비](#1-사전-준비)
2. [방법 A: 수동 Push (권장 — 가장 단순)](#2-방법-a-수동-push-권장--가장-단순)
3. [방법 B: GitLab Pull Mirroring (자동 동기화)](#3-방법-b-gitlab-pull-mirroring-자동-동기화)
4. [방법 C: Dual Remote Workflow (개발 중 동시 운영)](#4-방법-c-dual-remote-workflow-개발-중-동시-운영)
5. [GitLab 전용 후속 설정](#5-gitlab-전용-후속-설정)
6. [배지 및 CI 설정](#6-배지-및-ci-설정)
7. [동기화 유지 전략](#7-동기화-유지-전략)
8. [트러블슈팅](#8-트러블슈팅)
9. [체크리스트](#9-체크리스트)

---

## 1. 사전 준비

### 필수 조건

| 항목 | 상태 | 비고 |
|------|------|------|
| GitHub 레포 접근 | ✅ 완료 | `https://github.com/Two-Weeks-Team/duo-agentflow-auditor` |
| GitLab 계정 | 필요 | gitlab.com 계정 |
| 해커톤 그룹 접근 | 필요 | https://forms.gle/EeCH2WWUewK3eGmVA 에서 요청 |
| Git CLI | 필요 | `git --version` >= 2.x |

### 해커톤 그룹 접근 요청

```bash
# 1. 접근 요청 폼 제출
open "https://forms.gle/EeCH2WWUewK3eGmVA"

# 2. 승인 대기 (보통 24시간 이내)
# 3. 승인되면 https://gitlab.com/gitlab-ai-hackathon 접근 가능
```

> ⚠️ **블로커**: 접근 승인 없이는 프로젝트 생성 불가. 최우선 처리할 것.

### GitLab Personal Access Token 생성 (방법 B 필요 시)

1. GitLab → User Settings → Access Tokens
2. **Token name**: `github-mirror`
3. **Scopes**: `read_repository`, `write_repository`
4. **Expiration**: 해커톤 마감 이후 (2026-03-30)
5. 토큰 복사 및 안전한 곳에 저장

---

## 2. 방법 A: 수동 Push (권장 — 가장 단순)

**언제 사용**: 초기 1회 전송 + 이후 필요 시 수동 동기화. 대부분의 팀에 권장.

### Step 1: GitHub 레포 클론

```bash
git clone https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
cd duo-agentflow-auditor
```

### Step 2: GitLab 프로젝트 생성

1. https://gitlab.com/gitlab-ai-hackathon 접속
2. **New project** → **Create blank project**
3. 설정:

| 필드 | 값 |
|------|-----|
| Project name | `duo-agentflow-auditor` |
| Project slug | `duo-agentflow-auditor` |
| Visibility | **Public** |
| Initialize with README | ❌ **체크 해제** (중요! 충돌 방지) |

4. **Create project** 클릭
5. 생성된 프로젝트 URL 확인: `https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor`

### Step 3: GitLab Remote 추가 및 Push

```bash
# GitLab을 두 번째 remote로 추가
git remote add gitlab https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git

# 확인
git remote -v
# origin   https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (fetch)
# origin   https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (push)
# gitlab   https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git (fetch)
# gitlab   https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git (push)

# GitLab으로 Push
git push gitlab main

# 태그가 있으면 태그도 Push
git push gitlab --tags
```

### Step 4: 확인

```bash
# GitLab 프로젝트 페이지에서 확인할 항목:
# ✅ 파일 목록이 GitHub과 동일
# ✅ README.md가 제대로 렌더링
# ✅ LICENSE가 MIT로 표시
# ✅ agents/*.yml, flows/*.yml 존재
```

### 이후 동기화 (필요 시)

```bash
# GitHub에서 최신 가져오기
git pull origin main

# GitLab으로 전송
git push gitlab main
```

---

## 3. 방법 B: GitLab Pull Mirroring (자동 동기화)

**언제 사용**: GitHub에서 주로 개발하고, GitLab이 자동으로 따라오게 하고 싶을 때.

> ⚠️ GitLab Pull Mirroring은 **Premium/Ultimate** 플랜에서만 사용 가능.
> 해커톤 샌드박스가 이 기능을 지원하는지 확인 필요.

### Step 1: GitLab 프로젝트 생성 (방법 A의 Step 2와 동일)

빈 프로젝트로 생성 (README 초기화 해제).

### Step 2: Repository Mirroring 설정

1. GitLab 프로젝트 → **Settings** → **Repository**
2. **Mirroring repositories** 섹션 확장
3. 설정:

| 필드 | 값 |
|------|-----|
| Git repository URL | `https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git` |
| Mirror direction | **Pull** |
| Authentication method | None (public repo) |
| Only mirror protected branches | ❌ 체크 해제 |
| Keep divergent refs | ✅ 체크 |

4. **Mirror repository** 클릭

### Step 3: 동기화 확인

- 자동 동기화 주기: **5분마다** (GitLab 기본)
- 수동 즉시 동기화: Mirror 설정 옆 **Update now** 버튼

### Step 4: 동기화 상태 확인

```
Settings → Repository → Mirroring repositories
  Status: ✅ Last successful update: YYYY-MM-DD HH:MM
```

### 주의사항

- Pull Mirror가 활성화되면 **GitLab에서 직접 push 불가** (read-only)
- GitLab에서도 수정이 필요하면 → 방법 C(Dual Remote) 사용
- 해커톤 제출 직전에는 Mirror를 끄고 GitLab에서 직접 미세 조정 가능

---

## 4. 방법 C: Dual Remote Workflow (개발 중 동시 운영)

**언제 사용**: GitHub과 GitLab 양쪽 모두에서 적극적으로 개발할 때.

### 초기 설정

```bash
# 클론 (GitHub이 기본)
git clone https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
cd duo-agentflow-auditor

# GitLab remote 추가
git remote add gitlab https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git

# 양쪽 모두에 push하는 "all" remote 설정
git remote add all https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
git remote set-url --add --push all https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git
git remote set-url --add --push all https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git
```

### 확인

```bash
git remote -v
# all      https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (fetch)
# all      https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (push)
# all      https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git (push)
# gitlab   https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git (fetch)
# gitlab   https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor.git (push)
# origin   https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (fetch)
# origin   https://github.com/Two-Weeks-Team/duo-agentflow-auditor.git (push)
```

### 일상 워크플로우

```bash
# 개발: 평소처럼 작업
git add -A
git commit -m "feat: improve scanner prompt"

# 양쪽 동시 Push
git push all main

# 또는 개별 Push
git push origin main    # GitHub만
git push gitlab main    # GitLab만
```

### Git Alias 설정 (편의)

```bash
# ~/.gitconfig에 추가
git config --global alias.pushall '!git push origin main && git push gitlab main'

# 사용
git pushall
```

---

## 5. GitLab 전용 후속 설정

미러링 완료 후, GitLab에서 추가로 설정해야 할 항목들.

### 5-1. Duo Agent Platform 활성화

1. **Settings** → **General** → **Visibility, project features, permissions**
2. **GitLab Duo features** → 활성화
3. 저장 후 좌측 메뉴에 **Automate** 메뉴 확인:
   - Agents
   - Flows
   - Triggers
   - Sessions

### 5-2. 프로젝트 메타데이터

| 설정 위치 | 항목 | 값 |
|-----------|------|-----|
| Settings → General | Description | `Multi-agent security auditing flow for AI-assisted codebases` |
| Settings → General | Topics | `gitlab-duo`, `ai-agents`, `security`, `devsecops`, `hackathon` |
| Settings → General | Visibility | **Public** |
| Settings → General → Badges | License | MIT (자동 감지됨) |

### 5-3. 프로젝트 아바타 (선택)

1. **Settings** → **General** → **Project avatar**
2. 프로젝트 로고 업로드 (128x128 이상 권장)
3. 없으면 GitLab이 자동 생성한 아이콘 사용

### 5-4. Issues & MR 설정

| 설정 | 권장값 | 이유 |
|------|--------|------|
| Issues 활성화 | ✅ | DANGER 등급에서 자동 이슈 생성 |
| Merge Requests 활성화 | ✅ | Fix Agent가 MR 생성 |
| Wiki | ❌ 비활성화 가능 | 불필요 |
| Snippets | ❌ 비활성화 가능 | 불필요 |

---

## 6. 배지 및 CI 설정

### GitLab 프로젝트 배지 추가

1. **Settings** → **General** → **Badges**
2. 배지 추가:

| Badge Name | Link | Image URL |
|------------|------|-----------|
| License | `%{project_url}/-/blob/main/LICENSE` | `https://img.shields.io/badge/License-MIT-yellow.svg` |
| Platform | `https://docs.gitlab.com/user/duo_agent_platform/` | `https://img.shields.io/badge/Platform-GitLab%20Duo%20Agent-E24329` |
| Anthropic | `https://www.anthropic.com/` | `https://img.shields.io/badge/AI-Anthropic%20Claude-191919` |
| Agents | `%{project_url}/-/tree/main/agents` | `https://img.shields.io/badge/Agents-4-blue` |
| Rules | `%{project_url}/-/tree/main/rules` | `https://img.shields.io/badge/Detection%20Rules-26-red` |
| Green | `%{project_url}/-/blob/main/agents/metrics.md` | `https://img.shields.io/badge/Green%20Agent-Sustainability-228B22` |

### GitLab CI 파이프라인 (선택)

프로젝트에 CI 파이프라인을 추가하면 **Technological Implementation** 점수에 도움이 된다.

`.gitlab-ci.yml` 파일을 프로젝트 루트에 추가:

```yaml
stages:
  - validate
  - test

validate-yaml:
  stage: validate
  image: python:3.11-slim
  script:
    - python3 -c "
      import yaml, sys;
      f = open('flows/security-audit.yml');
      d = yaml.safe_load(f);
      assert d.get('definition', {}).get('version') == 'v1', 'Invalid schema version';
      assert 'components' in d.get('definition', {}), 'Missing components';
      assert 'routers' in d.get('definition', {}), 'Missing routers';
      print(f'✅ Flow YAML valid');
      "
  rules:
    - changes:
        - flows/*.yml

validate-rules:
  stage: validate
  image: python:3.11-slim
  script:
    - python3 -c "
      import json, sys;
      for f in ['rules/danger_rules.json', 'rules/warning_rules.json']:
        data = json.load(open(f));
        print(f'✅ {f}: {len(data)} rules');
        for r in data:
          assert 'category' in r, f'Missing category in {f}';
          assert 'regex' in r, f'Missing regex in {f}';
      "
  rules:
    - changes:
        - rules/*.json

lint-markdown:
  stage: test
  image: node:20-slim
  before_script:
    - npm install -g markdownlint-cli 2>/dev/null || true
  script:
    - markdownlint README.md CONTRIBUTING.md docs/*.md agents/*.md || true
  allow_failure: true
  rules:
    - changes:
        - "*.md"
        - "docs/*.md"
        - "agents/*.md"
```

---

## 7. 동기화 유지 전략

### 권장 워크플로우 (Phase별)

| Phase | 주 레포 | 동기화 방향 | 빈도 |
|-------|---------|-------------|------|
| **Phase 0** | GitHub → GitLab | 1회 (초기 미러링) | 1회 |
| **Phase 1-3** | GitHub (개발) → GitLab | 매일 또는 PR 머지 시 | 일 1-2회 |
| **Phase 4** | GitLab (에이전트 테스트) → GitHub | 프롬프트 수정 시 | 수시 |
| **Phase 5** | GitLab (최종) | GitLab이 최종본 | 제출 전 1회 확정 |

### 동기화 스크립트

프로젝트 루트에 `scripts/sync.sh` 추가 (선택):

```bash
#!/bin/bash
# GitHub → GitLab 동기화 스크립트
set -euo pipefail

echo "📥 Pulling from GitHub..."
git pull origin main --rebase

echo "📤 Pushing to GitLab..."
git push gitlab main

echo "✅ Sync complete: GitHub → GitLab"
echo "   GitHub: https://github.com/Two-Weeks-Team/duo-agentflow-auditor"
echo "   GitLab: https://gitlab.com/gitlab-ai-hackathon/<namespace>/duo-agentflow-auditor"
```

```bash
chmod +x scripts/sync.sh
./scripts/sync.sh
```

### 충돌 방지 규칙

| 규칙 | 이유 |
|------|------|
| GitHub에서만 코드 수정 | 단일 소스 보장 |
| GitLab에서는 에이전트/플로우 설정만 | UI 설정은 git으로 관리되지 않음 |
| 프롬프트 수정은 GitHub에서 → push → GitLab UI에서 반영 | 프롬프트 원본 관리 |
| Pull Mirror 사용 시 GitLab에서 직접 push 금지 | 충돌 발생 |

---

## 8. 트러블슈팅

### 미러링 관련

| 문제 | 원인 | 해결 |
|------|------|------|
| `rejected - non-fast-forward` | GitLab에 이미 커밋 존재 (README 초기화됨) | GitLab 프로젝트 삭제 후 재생성 (README 초기화 해제) 또는 `git push gitlab main --force` (최초 1회만) |
| `remote: HTTP Basic: Access denied` | 인증 실패 | `git remote set-url gitlab https://<username>:<token>@gitlab.com/...` |
| Pull Mirror "Last failed" | GitHub 접근 불가 | GitHub 레포가 Public인지 확인 |
| Pull Mirror "Pending" | 아직 첫 동기화 전 | **Update now** 클릭 또는 5분 대기 |

### 내용 불일치

| 문제 | 원인 | 해결 |
|------|------|------|
| GitLab에 파일 누락 | Push 안 됨 | `git push gitlab main` 재실행 |
| README 배지 깨짐 | shields.io 접근 불가 | 새로고침 — CDN 캐시 문제. 5분 후 정상화 |
| `.gitlab-ci.yml` 파이프라인 미실행 | CI 비활성화 | Settings → CI/CD → General pipelines → Enable |
| YAML 인코딩 오류 | BOM 문자 | 파일을 UTF-8 (no BOM)으로 재저장 |

### GitLab 특화

| 문제 | 원인 | 해결 |
|------|------|------|
| Automate 메뉴 안 보임 | Duo 미활성화 | Settings → General → GitLab Duo features 활성화 |
| 에이전트 생성 불가 | 권한 부족 | 해커톤 그룹에서 Maintainer 이상 역할 필요 |
| 플로우 YAML 에러 | 스키마 불일치 | `version: "v1"` 확인, 컴포넌트 이름에 하이픈(-) 대신 언더스코어(_) 사용 |
| 서비스 계정 미생성 | 플로우 미활성화 | Enable → Group + Project 선택 후 Save |

---

## 9. 체크리스트

### 미러링 완료 체크

- [ ] GitLab 프로젝트 URL 접근 가능
- [ ] 파일 목록이 GitHub과 100% 동일
- [ ] README.md 정상 렌더링 (배지 포함)
- [ ] LICENSE: MIT 표시
- [ ] `agents/*.yml` 및 `flows/security-audit.yml` 존재

### GitLab 후속 설정 체크

- [ ] Visibility: Public
- [ ] GitLab Duo features: 활성화
- [ ] Automate 메뉴: Agents, Flows, Triggers, Sessions 표시
- [ ] Project description 입력
- [ ] Topics 설정 (gitlab-duo, ai-agents, security 등)
- [ ] 배지 추가 (License, Platform, AI 등)

### CI 파이프라인 체크 (선택)

- [ ] `.gitlab-ci.yml` 추가
- [ ] validate-yaml Job 통과
- [ ] validate-rules Job 통과
- [ ] 파이프라인 배지가 프로젝트 페이지에 표시

### 제출 전 최종 체크

- [ ] GitLab 프로젝트가 **Public**
- [ ] MIT License가 프로젝트 페이지 상단에 표시
- [ ] 최신 코드가 GitLab에 반영 (`git push gitlab main`)
- [ ] 에이전트 4개 생성 + 활성화
- [ ] 플로우 생성 + 활성화 + 트리거 설정
- [ ] 데모 MR에서 end-to-end 동작 확인

---

## 요약: 어떤 방법을 선택해야 하나?

| 상황 | 권장 방법 | 이유 |
|------|-----------|------|
| 초기 전송만 필요 | **방법 A** (수동 Push) | 가장 단순, 오류 가능성 최소 |
| GitHub에서만 개발, GitLab은 자동 반영 | **방법 B** (Pull Mirror) | 설정 후 신경 안 써도 됨 |
| 양쪽 모두 적극 개발 | **방법 C** (Dual Remote) | `git push all` 한 줄로 동시 전송 |
| 잘 모르겠다 | **방법 A** | 복잡한 것 없이 확실하게 |
