"""Filter the Arabic table to the v0.0.21 source and fill its 14 missing strings."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("hushgram_l10n", ROOT / "scripts" / "gen-l10n.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)

EXTRA = {
    "Adds Details to a feed post's or reel's menu. It shows when it went up, who posted it, its media ID and the size Download saves, with buttons to copy the file link, username and caption.": "يضيف «التفاصيل» إلى قائمة منشور الموجز أو مقطع Reels. يعرض وقت النشر، وصاحب المنشور، ومعرّف الوسائط، وحجم الملف الذي يحفظه التنزيل، مع أزرار لنسخ رابط الملف واسم المستخدم والوصف.",
    "Adds Download full song under Download on reels that use a song from Instagram's music. It saves the whole song as an audio file, not only the part the reel plays.": "يضيف خيار «تنزيل الأغنية كاملة» أسفل «تنزيل» في مقاطع Reels التي تستخدم أغنية من مكتبة موسيقى Instagram. يحفظ الأغنية كاملة كملف صوتي، لا المقطع الذي يستخدمه الريلز فقط.",
    "Leaves out reels in the Reels tab with fewer views or likes than the numbers below. Reels from accounts you follow, reels sent to you and reels with no count still play.": "يخفي من تبويب Reels المقاطع التي تقل مشاهداتها أو إعجاباتها عن الأرقام المحددة أدناه. تبقى المقاطع من الحسابات التي تتابعها، والمُرسلة إليك، والتي لا يظهر لها عدد، متاحة.",
    "Lock single collections in Saved. A locked collection opens only once you unlock it the way Unlock with says. Saving a post to it never asks.": "يقفل مجموعات محددة في «المحفوظات». لا تُفتح المجموعة المقفلة إلا بعد إلغاء قفلها بالطريقة المحددة في «إلغاء القفل باستخدام». ولن يطلب منك تأكيدًا عند حفظ منشور فيها.",
    "Open a chat, tap the clock button at the top, or long press the chat's name, and pick Export chat. The whole chat is saved as a text file in Downloads, HushGram folder, one line per message.": "افتح محادثة، واضغط زر الساعة في أعلاها أو اضغط مطولًا على اسم المحادثة، ثم اختر «تصدير المحادثة». تُحفظ المحادثة كاملة كملف نصي في مجلد HushGram داخل التنزيلات، بحيث تكون كل رسالة في سطر.",
    "Open a collection in Saved, then come back here to lock it.": "افتح مجموعة في «المحفوظات»، ثم عُد إلى هنا لقفلها.",
    "Open a creator's profile from a reel, then their Reels tab, and it scrolls to that reel and outlines it for a moment. A photo reel is found in their posts. Stop looking ends the search where it is.": "افتح الملف الشخصي لصاحب المقطع من Reels، ثم تبويب Reels لديه؛ سينتقل إلى ذلك المقطع ويحدد إطاره للحظة. إذا كان المقطع صورة، فسيبحث عنه ضمن منشوراته. ينهي «إيقاف البحث» العملية عند موضعها الحالي.",
    "Puts a Download button at the top of a story, beside the three dots. One tap saves the photo or video in front, the same as Download in the menu.": "يضع زر «تنزيل» أعلى القصة بجانب النقاط الثلاث. اضغطه مرة واحدة لحفظ الصورة أو الفيديو المعروض، تمامًا مثل خيار التنزيل في القائمة.",
    "Reels with fewer views than this are left out. Type a whole number.": "يتم إخفاء مقاطع Reels التي يقل عدد مشاهداتها عن هذا الرقم. أدخل عددًا صحيحًا.",
    "Takes the accounts Instagram suggests off the bottom of your messages. Your chats and follow requests stay. Restart Instagram to see the change.": "يزيل الحسابات التي يقترحها Instagram أسفل الرسائل. تبقى محادثاتك وطلبات المتابعة كما هي. أعد تشغيل Instagram لتطبيق التغيير.",
    "Tells Instagram your phone has no AV1 decoder, so reels and stories come as VP9 or H.264, both to watch and to save. Takes a restart.": "يخبر Instagram أن هاتفك لا يدعم فك ترميز AV1، لذلك تُعرض مقاطع Reels والقصص بصيغتي VP9 أو H.264، سواء للمشاهدة أو الحفظ. يتطلب إعادة التشغيل.",
    "Videos on Home play with their sound on, the same as tapping a video's speaker. Mute one and the ones after it stay muted. Your phone's ringer and volume still count, so on silent or with the volume down, they stay quiet.": "تبدأ فيديوهات الصفحة الرئيسية بالصوت، كما لو ضغطت زر مكبر الصوت. إذا كتمت أحدها، تبقى الفيديوهات التالية مكتومة. يظل وضع رنين الهاتف ومستوى الصوت مؤثرين؛ فإذا كان الهاتف صامتًا أو مستوى الصوت منخفضًا، فستظل مكتومة.",
    "Videos, reels and stories play at the quality below, starting with the next one you open. When your connection can't keep up, a video drops to the next lower quality.": "تُشغّل الفيديوهات ومقاطع Reels والقصص بالجودة المحددة أدناه، بدءًا من المقطع التالي الذي تفتحه. إذا لم يتحمل اتصالك الجودة الحالية، تنخفض جودة الفيديو إلى المستوى الأدنى.",
    "Words or phrases, with a comma or a new line between them. Capital letters don't matter, and a hashtag works too.": "كلمات أو عبارات تفصل بينها فاصلة أو سطر جديد. لا يهم استخدام الأحرف الكبيرة أو الصغيرة، ويمكنك استخدام الوسوم أيضًا.",
}

table = Path(generator.L10N) / "ar.tsv"
entries = generator.read(table)
keys, others = generator.source_catalog(ROOT)
allowed = generator.allowed_keys(keys, others)

for key, value in EXTRA.items():
    if key in allowed and key not in entries:
        entries[key] = value

missing = keys - entries.keys()
if missing:
    raise SystemExit("Still missing Arabic translations:\n" + "\n".join(sorted(missing)))

removed = entries.keys() - allowed
for key in removed:
    del entries[key]

header = [
    "# Arabic for HushGram v0.0.21: the English key, a tab, the Arabic translation.",
    "# Filtered to the strings present in this release and completed with its 14 missing translations.",
    "# Translated by hamedhani1998: https://github.com/hamedhani1998/HushGram (PR #817, commit 1503f20f58f59b1efc2a36609227be19a8441abd). GPL-3.0-only.",
]
body = [generator.encode_field(key) + "\t" + generator.encode_field(entries[key]) for key in sorted(entries)]
table.write_text("\n".join(header + body) + "\n", encoding="utf-8", newline="\n")
print(f"Arabic v0.0.21 table ready: {len(entries)} entries; removed {len(removed)} entries from later releases.")
