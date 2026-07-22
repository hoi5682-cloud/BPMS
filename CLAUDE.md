# BPMS 프로젝트 — Figma 연동 규칙

> `10-projects/12-bpms` 전용 지침. SAP 통합 fit&gap용 AS-IS 프로세스를 BPMN 2.0 표기법으로 Figma에 문서화하는 프로젝트.
> 전체 배경·진행 상태는 [progress.md](./progress.md) 참조.

## 이 프로젝트의 성격 (먼저 확인할 것)

이 프로젝트는 **웹/앱 코드베이스가 아니다.** React/Vue 컴포넌트, CSS, 빌드 시스템, 아이콘 임포트 같은 개발자 중심 디자인 시스템 요소는 이 저장소 안에 존재하지 않는다. 실체는 **BPMN 다이어그램 그 자체(Figma 파일)** 이고, 저장소에는 그 원본 소스(drawio)와 분석 스크립트만 있다.

따라서 아래 항목들은 일반적인 "코드 프로젝트 + Figma" 통합 문서와 다르게, "적용 안 됨(N/A)"으로 명시하거나 이 프로젝트에 맞게 재정의했다.

## 1. 토큰 정의 (Design Tokens)

전통적 토큰 파일(색상/타이포/스페이싱 JSON 등)은 없음. 대신 **BPMN 도형 어휘가 토큰 역할**을 한다. 확정된 규칙(progress.md "최종 확정 스타일(E)", 2026-07-22 확정, 사용자 승인 완료)은 다음과 같다.

| 의미 | 도형 | 비고 |
|------|------|------|
| 시작/종료 (Event) | 원 (ellipse) | |
| 수동 Task | 흰 사각형 | |
| 시스템 Task | 색 채움 사각형 + 시스템 배지 | 배지 예: "SAP SD", "3PL/GTM" |
| 분기 (Decision) | 마름모 | 3개 이상 분기 시 배타적/포괄적 게이트웨이 표기를 명확히 구분 |
| 데이터 | 평행사변형, 연노랑 | |
| 문서 | 물결 밑단 도형, 연카키 | |
| 예외/긴급 | 빨간 점선 + 빨간 커넥터 | |
| 레인 구분 | 레인별 컬러 코드 | 시스템 구분은 색만으로 부족 → 배지 병기 (사용자 피드백 반영) |

원본 drawio의 도형 분류 로직(`_analysis/parse_drawio.py`의 `classify()`)이 이 어휘의 근거: `rhombus`→decision, `shape=parallelogram`→data, `shape=mxgraph.basic.document`/`document2`→document, `ellipse`→event, `fillColor=#FF3333` 또는 `sketch=1`→exception, `fillColor=#CCE5FF`→system-task로 매핑되어 있음.

## 2. 컴포넌트 라이브러리

코드 컴포넌트 없음. **Figma 네이티브 컴포넌트(심볼 세트)** 로 위 도형 어휘를 재사용 가능하게 만드는 것이 이번 라운드의 핵심 산출물(progress.md 계획 2단계). 위치는 저장소가 아니라 Figma 파일 자체:

- Figma 파일: https://www.figma.com/design/ko7I2wdTJFCretaPh6PmbK ("bpms — R1 AS-IS 스타일 비교")

Storybook 등 문서화 도구 없음 — 범례(legend)를 다이어그램 안에 포함하는 것으로 대체(합격 기준에 명시).

## 3. 프레임워크 & 라이브러리

UI 프레임워크·번들러·빌드 시스템 없음. 저장소에 있는 유일한 코드는 `_analysis/parse_drawio.py` (Python, 표준 라이브러리 `xml.etree.ElementTree`만 사용) — 원본 drawio XML을 파싱해 노드/엣지를 JSON으로 추출하는 1회성 분석 스크립트이며, 애플리케이션 코드가 아님.

## 4. 자산 관리

- 원본 소스: `제목 없는 다이어그램.drawio` (mxGraph XML, 199 vertices / 79 edges, 14개 프로세스 레인)
- 분석 산출물: `_analysis/drawio_parsed.json` (노드/엣지를 class·좌표와 함께 구조화)
- 최종 산출물: Figma 파일 (클라우드 자동저장). 필요 시 PNG/PDF export해서 fit&gap 워크숍 자료에 첨부(progress.md "내보내기 경로")
- CDN·이미지 최적화 파이프라인 없음

## 5. 아이콘 시스템

별도 아이콘 임포트 체계 없음. BPMN 도형 자체(위 1번 표)가 아이콘 역할을 겸함 — 시스템 배지 텍스트("SAP SD" 등)로 시스템 종류를 명시.

## 6. 스타일링 방식

CSS/스타일링 프레임워크 없음. "스타일"은 위 1번 토큰 표로 대체. 반응형 개념 없음(정적 다이어그램). 한 화면에 안 들어갈 만큼 레인이 많아지면 페이지 분할 규칙을 정해서 대응(합격 기준에 명시, 세부 규칙은 아직 미확정).

## 7. 프로젝트 구조

```
10-projects/12-bpms/          # 별도 git 저장소(hoi5682-cloud/bpms)로 관리
├── progress.md                # do-better-drive 진행 기록 (프레임→범위→계획→생산→검토→내보내기→회고)
├── 제목 없는 다이어그램.drawio  # 원본 AS-IS 소스 (draw.io)
├── _analysis/
│   ├── parse_drawio.py         # drawio XML → JSON 파서
│   └── drawio_parsed.json      # 파싱 결과
└── CLAUDE.md                   # 이 파일
```

## Figma MCP 사용 시 유의점

- Code Connect 대상 코드 컴포넌트가 없으므로 `get_code_connect_map`류는 해당 없음.
- `use_figma`로 다이어그램을 생성/수정할 때는 위 1번 도형 어휘·레인 컬러+배지 규칙을 그대로 따를 것 — 임의로 새 시각 언어를 추가하지 않는다.
- 원본 프로세스 내용(순서·조건분기)은 `_analysis/drawio_parsed.json`과 progress.md의 "추출된 해피패스 후보"가 근거 — 새로 인터뷰하지 않고 이 데이터를 그대로 재사용한다.
- 진행 중 미해결 질문 3건(레인 공백 여부·미배치 도형 8+5개·순서 검증, progress.md 참조)은 사람(kwan) 확인 전까지 임의로 확정하지 않는다.
