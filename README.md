# BPMS — Repair AS-IS 프로세스 표준화

## 목적

SAP 글로벌 시스템 통합의 fit&gap 분석을 위해 Repair 서비스의 AS-IS 프로세스를 BPMN 2.0 표기법으로 정리한다. 첫 라운드에서는 R1을 재구성하고 이후 시나리오에 재사용할 Figma 컴포넌트와 시각 기준을 확립한다.

## 현재 산출물

- Figma: `bpms — R1 AS-IS 스타일 비교`
- 원본: `제목 없는 다이어그램.drawio`
- 파싱 결과: `_analysis/drawio_parsed.json`
- 현재 상태와 미해결 질문: `progress.md`

## 주요 파일

- `progress.md` — 현재 단계, 결정, 사용자 확인 질문
- `CLAUDE.md` — BPMN 도형 어휘와 Figma 연동 규칙
- `AGENTS.md` — Codex 작업 규칙
- `_analysis/parse_drawio.py` — drawio XML 분석기

## 사용 및 검증

파서는 Python 표준 라이브러리만 사용한다. 파서나 원본을 변경하면 실제 drawio 파일로 실행해 JSON이 생성되는지 확인한다. 다이어그램은 원본 프로세스의 순서와 조건분기를 보존하고, 확정된 E안의 BPMN 도형 어휘를 일관되게 사용해야 한다.

## 데이터·보안

저장소와 Figma 산출물에 회사 기밀, 개인정보, 인증정보를 추가하기 전에 공유 가능 범위를 확인한다. `.env`, 키 파일과 로컬 도구 상태는 Git에 포함하지 않는다.

## 진행 상황

현재 단계와 다음 질문은 `progress.md`를 기준으로 한다. 이 폴더는 독립 Git 저장소이므로 상위 워크스페이스와 별도로 커밋하고 동기화한다.
