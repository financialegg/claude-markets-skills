<div dir="rtl">

# Claude Markets Skills

שישה סקילים בעברית שמלמדים את Claude לנתח חברות ציבוריות בצורה מסודרת: לא ממציא מספרים, מפריד בין עובדות להנחות, ומחשב בקוד ולא בראש.

מבית [הביצה הפיננסית](https://financialegg.co.il).

> חומר לימוד בלבד. אין כאן ייעוץ השקעות, המלצה לקנות או למכור, או תחזית. AI יכול לטעות. כל החלטה בידיים שלך.

## מה בפנים

**research-rules:** כללי עבודה לכל ניתוח. מקור ותאריך לכל מספר, ארבע תוויות (עובדה, ניתוח, הנחה, תרחיש), ו"מה חסר" בסוף.

**dcf:** הערכת שווי בשיטת DCF עם סקריפט חישוב מאומת (`dcf.py`), טבלת רגישות ובדיקות סבירות.

**multiples:** מכפילים והשוואה לחברות דומות, עם כללי "מונה ומכנה מאותו סוג".

**ratios:** יחסים פיננסיים מתוך דוחות, עם דגש על מגמה ולא על יעד קבוע.

**earnings-quality:** בדיקת איכות רווחים: פער בין רווח לתזרים, התאמות "מתואמות", תגמול מבוסס מניות.

**charts:** גרפים בעברית ב-matplotlib, עם הסבר מתחת לכל גרף.

## התקנה

### דרך א: Claude Code (שתי פקודות)

```
claude plugin marketplace add financialegg/claude-markets-skills
claude plugin install markets@financialegg
```

אחרי ההתקנה פותחים סשן חדש. הסקילים נטענים אוטומטית כשהבקשה מתאימה.

### דרך ב: תנו ל-Claude להתקין

בסשן של Claude Code, הדביקו:

```
התקן לי את התוסף markets מהריפו financialegg/claude-markets-skills.
הרץ: claude plugin marketplace add financialegg/claude-markets-skills
ואז: claude plugin install markets@financialegg
ספר לי כשסיימת.
```

### דרך ג: Claude Desktop

בהגדרות התוספים, מוסיפים Marketplace מריפוזיטורי GitHub ומזינים `financialegg/claude-markets-skills`, ואז מתקינים את `markets`. שמות התפריטים משתנים בין גרסאות.

### דרך ד: ידנית, בלי פלאגין

מורידים את הריפו (Code, ואז Download ZIP), ומעתיקים את התיקיות שבתוך `plugins/markets/skills/` אל `~/.claude/skills/` (ב-Windows: `C:\Users\<שם>\.claude\skills`).

## דוגמאות לשימוש

```
תנתח את דוח הרבעון האחרון של NVDA ותבדוק איכות רווחים
```

```
תבנה DCF לחברה הזו. הנה התזרימים והנחות הצמיחה שלי: ...
```

```
תשווה את המכפילים של AMD ו-INTC לשאר ענף השבבים ותצייר גרף
```

## בדיקה

הסקריפט `plugins/markets/skills/dcf/scripts/dcf.py` נבדק בעצמו:

```
python plugins/markets/skills/dcf/scripts/dcf.py --selftest
```

## רישיון

MIT. ראו [LICENSE](./LICENSE).

</div>
