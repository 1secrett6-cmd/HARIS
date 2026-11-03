# NEXORA Water Portfolio — 31 مشروعًا لأمن الأردن المائي

كل المشاريع مكتوبة كبيانات منظمة في `data/`، وكل الملفات (الكتاب التفصيلي، لوحات نموذج العمل، دراسات الجدوى، البروبوزلات، العرض التقديمي، المحاكي) تُولَّد منها تلقائيًا حتى تبقى الأرقام متطابقة.

## البنية

| الملف | الوظيفة |
|---|---|
| `data/p01_08.py` … `data/p25_31.py` | بيانات المشاريع الـ 31 (المشكلة، الحل، المميزات، BMC، الافتراضات المالية) |
| `common.py` | النموذج المالي لـ 3 سنوات، التنسيق، الطباعة إلى PDF |
| `build_book.py` | الكتاب التفصيلي `out/01_Water_Projects_Book.pdf` |
| `build_bmc.py` | لوحات نموذج العمل `out/02_Business_Model_Canvas.pdf` |
| `build_feasibility.py` | دراسات الجدوى `out/03_Feasibility_Studies.pdf` |
| `build_proposals.py` | 31 بروبوزل منفصل في `out/proposals/` |
| `build_deck.py` | العرض التقديمي `out/05_Pitch_Deck.pdf` و `.pptx` |
| `demos.py` + `sim/` + `build_sim.py` | المحاكيات: `out/simulators/index.html` (31 محاكي) و `out/simulators/dami.html` (تطبيق ذمي مع توصيل الدم بالدرون) |

## التشغيل

```bash
cd NEXORA-water
mkdir -p out
for s in book bmc feasibility proposals deck sim; do python3 build_$s.py; done
```

يحتاج Chromium (المسار في `common.py`).

المحاكيات ملفات HTML مستقلة تعمل بدون إنترنت: افتحها بأي متصفح.

## الحالة

- [x] بيانات المشاريع الـ 31
- [x] النموذج المالي
- [x] مولّد الكتاب التفصيلي
- [x] لوحات نموذج العمل (BMC)
- [x] دراسات الجدوى
- [x] البروبوزلات
- [x] العرض التقديمي (PDF + PPTX)
- [x] المحاكي التفاعلي

> جميع الأرقام المالية افتراضات تخطيطية أولية وليست أبحاث سوق؛ يجب التحقق منها قبل أي قرار.
