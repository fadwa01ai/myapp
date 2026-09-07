# 🐍 Snake Cosmic Maze HD

لعبة ثعبان (Snake) بتصميم كوني غامر، مبنية بـ Streamlit مع لعبة HTML5/Canvas مضمّنة داخلها.
تدعم لوحة المفاتيح (الأسهم أو WASD)، وأزرار اللمس والسحب (Swipe) على الجوال، ولوحة صدارة لأفضل 3 لاعبين.

## ✨ المزايا
- متاهة (Maze) بعوائق ثابتة.
- لوحة صدارة Top 3 محفوظة محلياً في المتصفح (localStorage).
- تحكم كامل بالأسهم / WASD على الكمبيوتر، وأزرار لمس + سحب على الجوال.
- تصميم مظلم بستايل "كوني" مع تأثيرات توهج (glow).

## 🚀 التشغيل محلياً

```bash
pip install -r requirements.txt
streamlit run app.py
```

بعدها افتح الرابط اللي يطلع لك في التيرمنال (عادة `http://localhost:8501`).

## ☁️ النشر على Streamlit Community Cloud

1. ارفع الملفين `app.py` و `requirements.txt` على مستودع GitHub.
2. ادخل على [share.streamlit.io](https://share.streamlit.io).
3. اربط حسابك بـ GitHub واختر المستودع.
4. حدد `app.py` كملف رئيسي (Main file path) واضغط Deploy.

## 📁 هيكل المشروع

```
.
├── app.py             # كود التطبيق واللعبة
├── requirements.txt   # المتطلبات
└── README.md
```

## ⚠️ ملاحظة عن لوحة الصدارة
النتائج تُحفظ عبر `localStorage` الخاص بمتصفح كل زائر، أي أنها **محلية لكل جهاز/متصفح** وليست
مشتركة بين اللاعبين على الإنترنت. لعمل لوحة صدارة عالمية حقيقية تحتاج قاعدة بيانات خلفية
(مثل Firebase أو Supabase) بدل الاعتماد على `localStorage`.
