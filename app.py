import os
import requests
import streamlit as st
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد واجهة الصفحة
st.set_page_config(
    page_title="تطبيق حالة الطقس", page_icon="🌤️", layout="centered"
)

# الحصول على المفتاح
API_KEY = os.getenv("OPENWEATHER_API_KEY", "c6d70c633d683ca39ce0fd8a91b19da7")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city_name):
    params = {"q": city_name, "appid": API_KEY, "units": "metric", "lang": "ar"}
    try:
        response = requests.get(BASE_URL, params=params)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)


st.title("🌤️ تطبيق حالة الطقس")
st.write("أدخل اسم المدينة لمعرفة حالة الطقس الحالية فوراً.")

city = st.text_input("اسم المدينة:", placeholder="مثال: الرياض، القاهرة، دبي")

if st.button("عرض حالة الطقس", type="primary"):
    if not city.strip():
        st.warning("يرجى إدخال اسم المدينة أولاً.")
    else:
        with st.spinner("جاري جلب بيانات الطقس..."):
            status, data = fetch_weather(city.strip())

            if status == 200:
                city_name = data["name"]
                country = data["sys"]["country"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"].capitalize()
                wind_speed = data["wind"]["speed"]
                icon_code = data["weather"][0]["icon"]
                icon_url = (
                    f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                )

                st.success(f"حالة الطقس في {city_name} ({country})")

                col_icon, col_desc = st.columns([1, 3])
                with col_icon:
                    st.image(icon_url, width=100)
                with col_desc:
                    st.subheader(description)

                col1, col2, col3 = st.columns(3)
                col1.metric(
                    "درجة الحرارة", f"{temp} °C", f"الشعور {feels_like} °C"
                )
                col2.metric("الرطوبة", f"{humidity}%")
                col3.metric("سرعة الرياح", f"{wind_speed} م/ث")

            elif status == 404:
                st.error(
                    f"لم يتم العثور على المدينة '{city}'. تأكد من كتابة الاسم بشكل صحيح."
                )
            elif status == 401:
                st.error("مفتاح الـ API غير صالح أو غير مفعّل بعد.")
            else:
                st.error("حدث خطأ أثناء الاتصال بالخدمة. يرجى المحاولة لاحقاً.")

st.markdown("---")
st.caption("تم التطوير باستخدام Python & Streamlit 🚀")