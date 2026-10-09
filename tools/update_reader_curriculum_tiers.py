import os
import re

path = r'c:\GitHub\Gurukuladesam\assets\js\books-reader.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace schedules block from `const PRIMARY_TRIMESTER_SCHEDULE = [` up to `function getOriginalSheetsForGrade(grade) {`
schedules_code = '''const GRADE_1_2_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: விளையாடிப் பயிலல் & 3 Ds கடமை (Play, Share & 3 Ds Action)',
    desc: 'நற்செயல் • அத் 1-3 • விளையாட்டு வழிக் கற்றல், பகிர்தல், உள்ளதைக் கொண்டு மகிழ்தல், கடமை-கட்டுப்பாடு-கண்ணியம்',
    checkpoint: '🎯 மாதம் 1 பால சாதனா ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: விளையாட்டும் மழலை மகிழ்ச்சியும்',
        theme: 'நற்செயல் அத் 1 • விளையாடுதல், பகிர்தல் & உள்ளதைக் கொண்டு மகிழ்தல்',
        lessons: [{ book: 'narcheyal', chap: 1 }]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: உணவு வீணாக்காத மழலைக் கடமை',
        theme: 'நற்செயல் அத் 2 • உணவை வீணாக்காமல் உண்ணும் நற்பழக்கம்',
        lessons: [{ book: 'narcheyal', chap: 2 }]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: விடியற்காலை எழும் கட்டுப்பாடு',
        theme: 'நற்செயல் அத் 3 • சூரிய உதயத்தில் எழுதல் & காலை வணக்கம்',
        lessons: [{ book: 'narcheyal', chap: 3 }]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: மாதம் 1 நற்செயல் ஆய்வு & 3 Ds பயிற்சி',
        theme: 'நற்செயல் அத் 3 • காலை விழிப்பு & விளையாடிப் பகிர்தல் செயல்முறைப் பயிற்சி',
        milestone: 'மாதம் 1 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [{ book: 'narcheyal', chap: 3 }]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: பள்ளி ஒழுக்கமும் தூய்மையும் (School Reverence & Cleanliness)',
    desc: 'நற்செயல் • அத் 4-5 • பள்ளிக்கு ஒழுங்காகச் செல்லுதல், காலணிகளை அடுக்குதல் & தூய்மை',
    checkpoint: '🎯 மாதம் 2 பால நற்செயல் ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: பள்ளிக்கு ஒழுங்காகச் செல்லுதல்',
        theme: 'நற்செயல் அத் 4 • ஆசிரியர் பணிவு, நேரந் தவறாமை & சுறுசுறுப்பு',
        lessons: [{ book: 'narcheyal', chap: 4 }]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: சுறுசுறுப்பும் சோம்பலின்மையும்',
        theme: 'நற்செயல் அத் 4 • சோம்பல் தவிர்த்து மகிழ்வோடு கற்றல்',
        lessons: [{ book: 'narcheyal', chap: 4 }]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: காலணிகளை அடுக்குதல் & தூய்மை',
        theme: 'நற்செயல் அத் 5 • உடைமைகள் பாதுகாப்பு & சுற்றுப்புறத் தூய்மை',
        lessons: [{ book: 'narcheyal', chap: 5 }]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: மாதம் 2 பால சாதனா ஆய்வு',
        theme: 'நற்செயல் அத் 5 • தூய்மை ஒழுக்கமும் சுயக் கட்டுப்பாடும்',
        milestone: 'மாதம் 2 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [{ book: 'narcheyal', chap: 5 }]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: தோழர் கண்ணியமும் புன்னகையும் (Friendship Dignity & Smile)',
    desc: 'நற்செயல் • அத் 6-7 • தோழர்களிடம் கண்ணியமாக விளையாடுதல், புன்னகை & நிறைவு',
    checkpoint: '🎓 மழலைப் பருவ நிறைவு & பட்டயம் (Infant Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: தோழர்களிடம் கண்ணியமாக விளையாடுதல்',
        theme: 'நற்செயல் அத் 6 • விட்டுக்கொடுத்தல், பகிர்தல் & கண்ணியமான விளையாட்டு',
        lessons: [{ book: 'narcheyal', chap: 6 }]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: சண்டை போடாமல் சமாதானம்',
        theme: 'நற்செயல் அத் 6 • கோபமின்மை & தோழர் அன்பு',
        lessons: [{ book: 'narcheyal', chap: 6 }]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: புன்னகைக் கண்ணியமும் அமைதியும்',
        theme: 'நற்செயல் அத் 7 • அழுது அடம்பிடிக்காத புன்னகைக் கண்ணியம் & அமைதி',
        lessons: [{ book: 'narcheyal', chap: 7 }]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: மழலைப் பருவ நிறைவுப் பட்டய ஆய்வு',
        theme: 'நற்செயல் அத் 7 • நற்செயல் 7 அத்தியாயங்கள் முழு நிறைவு & 3 Ds வாழ்வியல் பயிற்சி',
        milestone: '🎓 மழலைப் பருவ நிறைவுப் பட்டயம் (Infant Term Diploma - 7 அத்தியாயங்கள்)',
        lessons: [{ book: 'narcheyal', chap: 7 }]
      }
    ]
  }
];

const GRADE_3_4_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நற்செயல் அடித்தளமும் 3 Ds கடமையும் (Action Foundation & 3 Ds)',
    desc: 'நற்செயல் • அத் 1-5 • விளையாட்டு வழிக் கற்றல், பகிர்தல், விடியற்காலை விழிப்பு & தூய்மை',
    checkpoint: '🎯 மாதம் 1 பால சாதனா ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: விளையாடிப் பகிர்தலும் உணவு உண்பதும்',
        theme: 'நற்செயல் அத் 1-2 • விளையாடுதல் & உணவை வீணாக்காமல் உண்ணும் கடமை',
        lessons: [
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: சூரிய உதயமும் விடியலில் எழும் கடமையும்',
        theme: 'நற்செயல் அத் 3 • விடியற்காலை எழும் கட்டுப்பாடு & காலை வணக்கம்',
        lessons: [
          { book: 'narcheyal', chap: 3 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: பள்ளிக்கு ஒழுங்காகச் செல்லுதல்',
        theme: 'நற்செயல் அத் 4 • சுறுசுறுப்பு & ஆசிரியர் பணிவு',
        lessons: [
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: தூய்மையும் உடைமைப் பாதுகாப்பும்',
        theme: 'நற்செயல் அத் 5 • காலணிகளை அடுக்குதல் & உடைமைத் தூய்மை',
        milestone: 'மாதம் 1 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [
          { book: 'narcheyal', chap: 5 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்செயல் நிறைவும் நற்பண்பு தொடக்கமும் (Action Completion & Noble Virtue)',
    desc: 'நற்செயல் அத் 6-7 & நற்பண்பு அத் 1-2 • கண்ணியமான விளையாட்டு, சுறுசுறுப்பு & உண்மை நெறி',
    checkpoint: '🎯 மாதம் 2 நற்பண்பு ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: தோழர்களிடம் கண்ணியமாக விளையாடுதல்',
        theme: 'நற்செயல் அத் 6 • பகிர்வு, விட்டுக் கொடுத்தல் & நேசமான தோழமை',
        lessons: [
          { book: 'narcheyal', chap: 6 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: புன்னகைக் கண்ணியமும் நற்செயல் நிறைவும்',
        theme: 'நற்செயல் அத் 7 • அழுது அடம்பிடிக்காத புன்னகை & நற்செயல் முழுமை',
        lessons: [
          { book: 'narcheyal', chap: 7 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: நற்பண்பும் நல்வழியில் நடப்பதும்',
        theme: 'நற்பண்பு அத் 1 • பெரியோர் வணக்கம், பணிவு & நல்வழி தொடக்கம்',
        lessons: [
          { book: 'nalvazhi', chap: 1 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: சுறுசுறுப்பும் சோம்பல் தவிர்த்தலும்',
        theme: 'நற்பண்பு அத் 2 • சுறுசுறுப்பான வாழ்க்கை & ஊக்கம்',
        milestone: 'மாதம் 2 நற்பண்பு தொடக்க ஆய்வு',
        lessons: [
          { book: 'nalvazhi', chap: 2 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்பண்பு மேன்மையும் தர்ம நிறைவும் (Noble Character & Dharma Graduation)',
    desc: 'நற்பண்பு அத் 3-7 • அறிவு, நல்ல தோழமை, அடக்கம், முயற்சி & நற்பெயர் காத்தல்',
    checkpoint: '🎓 தொடக்கப் பள்ளிப் பருவ நிறைவு & பட்டயம் (Primary Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: அறிவின் மேன்மை',
        theme: 'நற்பண்பு அத் 3 • கல்வி ஆர்வமும் நல்லறிவுத் தேடலும்',
        lessons: [
          { book: 'nalvazhi', chap: 3 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: நல்ல நண்பர்கள் சேர்க்கை',
        theme: 'நற்பண்பு அத் 4 • நற்குணத் தோழமையும் நற்பழக்கமும்',
        lessons: [
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: பணிவும் முயற்சியும்',
        theme: 'நற்பண்பு அத் 5-6 • அடக்கம் உடைமை & விடாமுயற்சியே செல்வம்',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: நற்பெயர் காத்தல் & தொடக்கப் பள்ளி நிறைவு',
        theme: 'நற்பண்பு அத் 7 • நற்பெயரைக் காத்து வாழ்தல் & 2 நூல்கள் முழு நிறைவு',
        milestone: '🎓 தொடக்கப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (Primary Term Diploma - 14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nalvazhi', chap: 7 }
        ]
      }
    ]
  }
];

const MIDDLE_SCHOOL_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நன்னெறி & நல்லறம் (Conduct & Righteous Deeds)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • பெரியோர் வழிபாடு, நற்பழக்கம், ஈகை & உயிரிரக்கம்',
    checkpoint: '🎯 மாதம் 1 அறநெறி ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் பணிவும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி & நற்குணம்',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: இன்சொல்லும் ஈகையும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம், பகிர்தல் & ஈகைக் குணம்',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை & இயற்கை பாதுகாப்பு',
        milestone: 'மாதம் 1 நன்னெறி & நல்லறத் தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்பண்பு & நற்துணை (Virtue, Truth & Divine Refuge)',
    desc: 'நற்பண்பு & நற்துணை • 14 அத்தியாயங்கள் • வாய்மை, உழைப்பு, தெய்வத் துதி & சரணாகதி',
    checkpoint: '🎯 மாதம் 2 நற்பண்பு & பக்தி ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை & உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: முயற்சி உணர்வும் இறை சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • அடக்கம், முயற்சி, நற்பெயர் காத்தல் & விநாயகர் துணை',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-4 • முருகன் வேல் துணை, சிவபெருமான் அருள் & அம்பிகை கருணை',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தெய்வ சரணாகதியும்',
        theme: 'நற்துணை அத் 5-7 • திருமால் அருள், ஆஞ்சநேயர் வீரம் & அபயம்',
        milestone: 'மாதம் 2 நற்பண்பு & நற்துணை ஆய்வு (28 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 5 },
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்செயல் & 3 Ds வாழ்வியல் நெறி (Practical Dharma & Graduation)',
    desc: 'நற்செயல் • 7 அத்தியாயங்கள் • கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity) & தர்ம வாழ்க்கை',
    checkpoint: '🎓 நடுநிலைப் பள்ளிப் பருவ நிறைவு & பட்டயம் (Middle School Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: விளையாடிப் பகிர்தலும் உணவு நெறியும்',
        theme: 'நற்செயல் அத் 1-2 • விளையாடுதல், பகிர்தல் & உணவு வீணாக்காத கடமை',
        lessons: [
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: அதிகாலை எழுச்சியும் பள்ளி ஒழுக்கமும்',
        theme: 'நற்செயல் அத் 3-4 • விடியற்காலை விழிப்பு, சூரிய நமஸ்காரம் & பள்ளி சுறுசுறுப்பு',
        lessons: [
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: தூய்மையும் தோழர் கண்ணியமும்',
        theme: 'நற்செயல் அத் 5-6 • தூய்மைப் பழக்கம் & தோழர்களிடம் கண்ணியமாகப் பழகுதல்',
        lessons: [
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: புன்னகைக் கண்ணியமும் நடுநிலைப் பள்ளிப் பட்டயமும்',
        theme: 'நற்செயல் அத் 7 • புன்னகைக் கண்ணியம் & 5 நூல்கள் முழுப் பருவ நிறைவு',
        milestone: '🎓 நடுநிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (Middle School Diploma - 35 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const HIGH_SCHOOL_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நன்னெறி & நல்லறம் (Right Conduct & Righteous Deeds)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • நற்பழக்கம், பெரியோர் பணிவு, ஈகை & ஜீவகாருண்யம்',
    checkpoint: '🎯 மாதம் 1 உயர் அறநெறி ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் வணக்கமும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி & நற்குணம்',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: நற்பழக்கங்களும் இன்சொல்லும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம், பகிர்வு & அறம் போற்றுதல்',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை & இயற்கை சூழல் பாதுகாப்பு',
        milestone: 'மாதம் 1 தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்பண்பு & நற்துணை (Virtue, Truth & Divine Refuge)',
    desc: 'நற்பண்பு & நற்துணை • 14 அத்தியாயங்கள் • வாய்மை, உழைப்பு, திருமுறை பக்தி & சரணாகதி',
    checkpoint: '🎯 மாதம் 2 வாய்மை & சரணாகதி ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை & உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: கடமை உணர்வும் சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • சோதனை வெல்லும் அறம், நற்பெயர் காத்தல் & விநாயகர் துணை',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-4 • முருகன் துணை, சிவபெருமான் திருவருள் & அம்பிகை பக்தி',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தெய்வ சரணாகதியும்',
        theme: 'நற்துணை அத் 5-7 • காக்கும் பெருமாள், ஆஞ்சநேயர் பக்தி & அபயம்',
        milestone: 'மாதம் 2 தேர்ச்சி ஆய்வு (28 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 5 },
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்சொல் & நற்செயல் (Sweet Speech & Practical Dharma)',
    desc: 'நற்சொல் & நற்செயல் • 14 அத்தியாயங்கள் • நாவடக்கம், இன்சொல், 3 Ds & பஞ்ச மகா யாகங்கள்',
    checkpoint: '🎓 உயர்நிலைப் பள்ளிப் பருவ நிறைவு & பட்டயம் (High School Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: நாவடக்கமும் இனிய மொழியும்',
        theme: 'நற்சொல் அத் 1-4 • இன்சொல் பேசுதல், புறங்கூறாமை & வாக்கின் தூய்மை',
        lessons: [
          { book: 'narchol', chap: 1 },
          { book: 'narchol', chap: 2 },
          { book: 'narchol', chap: 3 },
          { book: 'narchol', chap: 4 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: பயனுள்ள சொல்லும் தினசரி தர்மமும்',
        theme: 'நற்சொல் அத் 5-7 & நற்செயல் அத் 1 • பயன்படப் பேசுதல், கோபமின்மை & விளையாடிப் பகிர்தல்',
        lessons: [
          { book: 'narchol', chap: 5 },
          { book: 'narchol', chap: 6 },
          { book: 'narchol', chap: 7 },
          { book: 'narcheyal', chap: 1 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: உணவு நெறியும் விடியற்காலை எழும் கட்டுப்பாடும்',
        theme: 'நற்செயல் அத் 2-4 • உணவு வீணாக்காத கடமை, விடியற்காலை விழிப்பு & பள்ளி ஒழுக்கம்',
        lessons: [
          { book: 'narcheyal', chap: 2 },
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: 3 Ds செயல்முறை, பஞ்ச யாகங்கள் & பட்டமளிப்பு',
        theme: 'நற்செயல் அத் 5-7 • தூய்மை, தோழர் கண்ணியம், புன்னகை & 6 நூல்கள் முழு நிறைவு',
        milestone: '🎓 உயர்நிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (High School Diploma - 42 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 },
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const COLLEGIATE_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: அற அடித்தளமும் தர்ம ஒழுக்கமும் (Moral Foundation & Right Conduct)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • நற்பழக்கம், ஈகை & பெரியோர் பணிவு',
    checkpoint: '🎯 மாதம் 1 இடைப் பருவ ஆய்வு (Month 1 Milestone Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் வணக்கமும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: நற்பழக்கங்களும் இன்சொல்லும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம் & பகிர்வு',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை, சுற்றுப்புறப் பாதுகாப்பு',
        milestone: 'மாதம் 1 தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: பக்தி, இசை & மெய்யறிவு விழிப்பு (Devotion, Sacred Hymns & Wisdom)',
    desc: 'நற்பண்பு, நற்துணை & நற்சிந்தனை • 16 அத்தியாயங்கள் • வாய்மை, தேவாரம் & பிரபஞ்ச வியப்பு',
    checkpoint: '🎯 மாதம் 2 இடைப் பருவ ஆய்வு (Month 2 Milestone Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை, உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: கடமை உணர்வும் சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • சோதனை வெல்லும் அறம், இறை சரணாகதி',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-5 • விநாயகர், முருகன், சிவபெருமான், சக்தி வழிபாட்டுப் பாடல்கள்',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 },
          { book: 'narthunai', chap: 5 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தத்துவ ஆய்வும்',
        theme: 'நற்துணை அத் 6-7 & நற்சிந்தனை அத் 1-2 • அபயம், மன அமைதி & மெய்யறிவு வினாக்கள்',
        milestone: 'மாதம் 2 தேர்ச்சி ஆய்வு (30 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 },
          { book: 'narchinthanai', chap: 1 },
          { book: 'narchinthanai', chap: 2 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: வேதாந்த-அறிவியல், சமுதாயத் தொண்டு & இறுதிப் பட்டயம் (Higher Studies & Graduation)',
    desc: 'நற்சிந்தனை, நற்சொல் & நற்செயல் • 19 அத்தியாயங்கள் • விஞ்ஞான-மெய்ஞ்ஞானம், 3 Ds & பஞ்ச யாகங்கள்',
    checkpoint: '🎓 இறுதிப் பருவத் தேர்ச்சி & பட்டயம் (Term Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: விஞ்ஞானமும் பிரபஞ்ச தத்துவமும்',
        theme: 'நற்சிந்தனை அத் 3-6 • இயற்கை விதிகள், அண்டவெளி ஆச்சர்யம், அறிவியல் சங்கமம்',
        lessons: [
          { book: 'narchinthanai', chap: 3 },
          { book: 'narchinthanai', chap: 4 },
          { book: 'narchinthanai', chap: 5 },
          { book: 'narchinthanai', chap: 6 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: நாவடக்கமும் இனிய மொழியும்',
        theme: 'நற்சிந்தனை அத் 7 & நற்சொல் அத் 1-3 • இன்சொல் பேசுதல், புறங்கூறாமை, வாக்கின் தூய்மை',
        lessons: [
          { book: 'narchinthanai', chap: 7 },
          { book: 'narchol', chap: 1 },
          { book: 'narchol', chap: 2 },
          { book: 'narchol', chap: 3 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: பயனுள்ள சொல்லும் தினசரி தர்மமும்',
        theme: 'நற்சொல் அத் 4-7 & நற்செயல் அத் 1-2 • பயன்படப் பேசுதல், இல்லறக் கடமைகள் தொடக்கம்',
        lessons: [
          { book: 'narchol', chap: 4 },
          { book: 'narchol', chap: 5 },
          { book: 'narchol', chap: 6 },
          { book: 'narchol', chap: 7 },
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: 3 Ds செயல்முறை, பஞ்ச யாகங்கள் & பட்டமளிப்பு',
        theme: 'நற்செயல் அத் 3-7 • கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity), பஞ்ச மகா யாகங்கள் & முழுப் பருவ நிறைவு',
        milestone: '🎓 பருவ நிறைவுப் பட்டயச் சான்றிதழ் (Grade Term Diploma - 49 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 },
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 },
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const PRIMARY_TRIMESTER_SCHEDULE = GRADE_1_2_SCHEDULE;
const SECONDARY_TRIMESTER_SCHEDULE = COLLEGIATE_SCHEDULE;
const TRIMESTER_SCHEDULE = COLLEGIATE_SCHEDULE;

function getScheduleForGrade(grade) {
  if (grade <= 2) return GRADE_1_2_SCHEDULE;
  if (grade <= 4) return GRADE_3_4_SCHEDULE;
  if (grade <= 8) return MIDDLE_SCHOOL_SCHEDULE;
  if (grade <= 12) return HIGH_SCHOOL_SCHEDULE;
  return COLLEGIATE_SCHEDULE;
}'''

# Replace from `const PRIMARY_TRIMESTER_SCHEDULE = [` to `function getScheduleForGrade(grade) {\n  return (grade <= 5) ? PRIMARY_TRIMESTER_SCHEDULE : SECONDARY_TRIMESTER_SCHEDULE;\n}`
old_sched_pattern = r'const PRIMARY_TRIMESTER_SCHEDULE = \[[\s\S]*?function getScheduleForGrade\(grade\) \{\s*return \(grade <= 5\) \? PRIMARY_TRIMESTER_SCHEDULE : SECONDARY_TRIMESTER_SCHEDULE;\s*\}'
if not re.search(old_sched_pattern, content):
    print("ERROR: old_sched_pattern not matched!")
else:
    content = re.sub(old_sched_pattern, schedules_code, content, count=1)
    print("SUCCESS: Schedules updated!")

# 2. Update getGradeProgressMetrics levelTitle
old_metrics = '''  let levelTitle = 'பால சாதகன் (Young Seeker)';
  if (grade <= 5) {
    if (totalXp >= 2500) levelTitle = 'பால வித்வான் (Primary Master)';
    else if (totalXp >= 1500) levelTitle = 'பால நற்பண்பாளர் (Junior Scholar)';
    else if (totalXp >= 700) levelTitle = 'தர்ம பாலன் (Dharmic Child)';
    else if (totalXp >= 200) levelTitle = 'விளையாட்டு சாதகன் (Play & Learn Seeker)';
  } else {
    if (totalXp >= 6000) levelTitle = 'ஆசிரம வித்வான் (Ashram Master)';
    else if (totalXp >= 3500) levelTitle = 'குருகுல நற்பண்பாளர் (Gurukula Scholar)';
    else if (totalXp >= 1500) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else if (totalXp >= 500) levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  }'''

new_metrics = '''  let levelTitle = 'பால சாதகன் (Young Seeker)';
  if (grade <= 2) {
    if (totalXp >= 900) levelTitle = 'மழலை நற்செயல் வித்தகர் (Infant Action Master)';
    else if (totalXp >= 500) levelTitle = 'பால நற்செயல் சாதகன் (Young Action Seeker)';
    else if (totalXp >= 200) levelTitle = 'விளையாட்டு சாதகன் (Play & Learn Seeker)';
    else levelTitle = 'மழலை சாதகன் (Little Seeker)';
  } else if (grade <= 4) {
    if (totalXp >= 1800) levelTitle = 'பால தர்ம வித்வான் (Primary Dharma Master)';
    else if (totalXp >= 1000) levelTitle = 'பால நற்பண்பாளர் (Primary Virtue Scholar)';
    else if (totalXp >= 400) levelTitle = 'தர்ம பாலன் (Dharmic Student)';
    else levelTitle = 'பால சாதகன் (Young Seeker)';
  } else if (grade <= 8) {
    if (totalXp >= 4500) levelTitle = 'இளம் குருகுல வித்வான் (Junior Ashram Master)';
    else if (totalXp >= 2500) levelTitle = 'இளம் நற்பண்பாளர் (Middle School Scholar)';
    else if (totalXp >= 1000) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  } else if (grade <= 12) {
    if (totalXp >= 5500) levelTitle = 'உயர்நிலைக் குருகுல வித்வான் (Senior Gurukula Master)';
    else if (totalXp >= 3000) levelTitle = 'உயர்நிலை நற்பண்பாளர் (Senior Dharmic Scholar)';
    else if (totalXp >= 1200) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  } else {
    if (totalXp >= 6000) levelTitle = 'ஆசிரம வித்வான் (Ashram Master)';
    else if (totalXp >= 3500) levelTitle = 'குருகுல நற்பண்பாளர் (Gurukula Scholar)';
    else if (totalXp >= 1500) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  }'''

if old_metrics in content:
    content = content.replace(old_metrics, new_metrics)
    print("SUCCESS: getGradeProgressMetrics updated!")
else:
    print("ERROR: old_metrics not found!")

# 3. Update initClassroomApp mainTitle, termDesc, classworkTabTitle
old_titles = '''  const isPrimary = (grade <= 5);
  const hasOriginalSheets = (grade === 1 || grade === 2);

  const mainTitle = isPrimary
    ? `தரம் ${grade} — தொடக்கப் பள்ளி 3 மாதப் பருவம் (Primary 12-Week Academy)`
    : `தரம் ${grade} — 3 மாத காலப் பருவம் (12-Week Trimester Academy)`;

  const termDesc = isPrimary
    ? `பாலப் பருவம் • 3 முதன்மை ஆசிரமப் பாடநூல்கள் (நற்செயல், நல்வழி, நற்துணை) • 21 அத்தியாயங்கள் • விளையாடிப் பயிலல் &amp; 3 Ds நெறிமுறை`
    : `பருவம் 1 • 7 ஆசிரமப் பாடநூல்கள் • 49 அத்தியாயங்கள் • தினசரி சாதனா &amp; 3 Ds நெறிமுறை`;

  const classworkTabTitle = isPrimary
    ? `பாடப் பணிகள் (Classwork &amp; 3 Books)`
    : `பாடப் பணிகள் (Classwork &amp; 7 Books)`;'''

new_titles = '''  const hasOriginalSheets = (grade === 1 || grade === 2);

  let mainTitle = '';
  let termDesc = '';
  let classworkTabTitle = '';

  if (grade <= 2) {
    mainTitle = `தரம் ${grade} — மழலைப் பருவம் 3 மாதப் பயில்வு (Infant 12-Week Academy)`;
    termDesc = `மழலைப் பருவம் • 1 ஆசிரமப் பாடநூல் (நற்செயல்) • 7 அத்தியாயங்கள் • விளையாடிப் பயிலல், பகிர்தல் &amp; 3 Ds நெறிமுறை`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 1 நூல்)`;
  } else if (grade <= 4) {
    mainTitle = `தரம் ${grade} — தொடக்கப் பள்ளி 3 மாதப் பருவம் (Primary 12-Week Academy)`;
    termDesc = `பாலப் பருவம் • 2 முதன்மை ஆசிரமப் பாடநூல்கள் (நற்செயல், நற்பண்பு) • 14 அத்தியாயங்கள் • விளையாடிப் பயிலல் &amp; நற்பண்பு`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 2 நூல்கள்)`;
  } else if (grade <= 8) {
    mainTitle = `தரம் ${grade} — நடுநிலைப் பள்ளி 3 மாதப் பருவம் (Middle School 12-Week Academy)`;
    termDesc = `இளம் பருவம் • 5 ஆசிரமப் பாடநூல்கள் (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்செயல்) • 35 அத்தியாயங்கள் • தினசரி சாதனா &amp; 3 Ds`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 5 நூல்கள்)`;
  } else if (grade <= 12) {
    mainTitle = `தரம் ${grade} — உயர்நிலைப் பள்ளி 3 மாதப் பருவம் (High School 12-Week Academy)`;
    termDesc = `உயர்நிலைப் பருவம் • 6 ஆசிரமப் பாடநூல்கள் (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சொல், நற்செயல்) • 42 அத்தியாயங்கள் • தர்ம நெறி &amp; வாழ்வியல் சாதனா`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 6 நூல்கள்)`;
  } else {
    mainTitle = `உயர்கல்வி வித்யாபீடம் — 3 மாத காலப் பருவம் (Higher Studies 12-Week Academy)`;
    termDesc = `உயர்கல்விப் பருவம் • 7 ஆசிரமப் பாடநூல்கள் • 49 அத்தியாயங்கள் • வேத-நவீன அறிவியல் சங்கமம் &amp; 3 Ds நெறிமுறை`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 7 நூல்கள்)`;
  }'''

if old_titles in content:
    content = content.replace(old_titles, new_titles)
    print("SUCCESS: initClassroomApp titles updated!")
else:
    print("ERROR: old_titles not found!")

# 4. Update renderMasteryPanelHtml
old_mastery = '''function renderMasteryPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const activeBooks = getBooksMetadataForGrade(grade);
  const isPrimary = (grade <= 5);

  let html = `
    <div>
      <!-- Mastery Metrics Strip -->
      <div class="mastery-overview-strip">
        <div class="mastery-metric-card">
          <div class="mastery-metric-num">${metrics.totalChapters}</div>
          <div class="mastery-metric-label">பருவப் பாடங்கள் (Total Chapters)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#10b981;">${metrics.completedCount}</div>
          <div class="mastery-metric-label">வாசித்து உணர்ந்தவை (${metrics.percentage}%)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#38bdf8;">${metrics.totalXp.toLocaleString()}</div>
          <div class="mastery-metric-label">தர்ம சாதனா புள்ளிகள் (Vedic XP)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:var(--gold-bright);">${metrics.unlockedBadges} / ${metrics.totalBadges}</div>
          <div class="mastery-metric-label">நிறைவுப் பதக்கங்கள் (Ashram Badges)</div>
        </div>
      </div>

      <!-- Books Mastery Cards Grid -->
      <div style="margin: 20px 0 12px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="color:#ffffff; font-size:1.15rem; font-weight:800; margin:0;">
          ${isPrimary ? '3 முதன்மை ஆசிரம நூல்களின் தேர்ச்சி நிலை (Primary 3 Books Mastery)' : '7 ஆசிரம நூல்களின் தேர்ச்சி நிலை (7 Sacred Books Mastery)'}
        </h3>
        <span style="font-size:0.8rem; color:#94a3b8;">ஒவ்வொரு நூலிலும் 7 அத்தியாயங்கள்</span>
      </div>

      <div class="mastery-books-grid">
  `;

  activeBooks.forEach((book, idx) => {
    const done = metrics.bookMetrics[book.id] || 0;
    const isMastered = (done === 7);
    const pct = Math.round((done / 7) * 100);

    let dotsHtml = '';
    for (let c = 1; c <= 7; c++) {
      const cDone = isBookChapterCompleted(grade, book.id, c);
      dotsHtml += `<span class="mastery-dot ${cDone ? 'done' : ''}" title="அத்தியாயம் ${c}: ${cDone ? 'நிறைவு பெற்றது' : 'படிக்க வேண்டியுள்ளது'}"></span>`;
    }

    let badgeName = '';
    if (isPrimary) {
      const primaryBadges = {
        'narcheyal': '☀️ நற்செயல் கர்மவீரர் (Action Champion & 3 Ds)',
        'nalvazhi': '⭐ நல்வழி நேர்மையாளர் (Truth Bearer)',
        'narthunai': '🪔 நற்துணை மெய்ஞ்ஞானி (Divine Refuge)'
      };
      badgeName = primaryBadges[book.id] || `${book.name} தேர்ச்சிப் பதக்கம்`;
    } else {
      const secondaryBadges = [
        '🏅 நன்னெறி சுடர் (Conduct Pillar)',
        '🛡️ நல்லறச் செம்மல் (Dharma Champion)',
        '⚖️ நல்வழி வித்தகர் (Truth Bearer)',
        '🪔 நற்துணை யோகி (Divine Refuge)',
        '⚛️ நற்சிந்தனை ஞானி (Wisdom Seeker)',
        '🌸 நற்சொல் வள்ளல் (Sweet Word Master)',
        '☀️ நற்செயல் கர்மயோகி (Action Yogin)'
      ];
      badgeName = secondaryBadges[idx] || `${book.name} தேர்ச்சிப் பதக்கம்`;
    }'''

new_mastery = '''function renderMasteryPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const activeBooks = getBooksMetadataForGrade(grade);

  let masteryTitle = '7 ஆசிரம நூல்களின் தேர்ச்சி நிலை (7 Sacred Books Mastery)';
  if (grade <= 2) masteryTitle = '1 ஆசிரம நூலின் தேர்ச்சி நிலை (Infant 1 Book Mastery • நற்செயல்)';
  else if (grade <= 4) masteryTitle = '2 முதன்மை ஆசிரம நூல்களின் தேர்ச்சி நிலை (Primary 2 Books Mastery • நற்செயல், நற்பண்பு)';
  else if (grade <= 8) masteryTitle = '5 ஆசிரம நூல்களின் தேர்ச்சி நிலை (Middle School 5 Books Mastery)';
  else if (grade <= 12) masteryTitle = '6 ஆசிரம நூல்களின் தேர்ச்சி நிலை (High School 6 Books Mastery)';

  let html = `
    <div>
      <!-- Mastery Metrics Strip -->
      <div class="mastery-overview-strip">
        <div class="mastery-metric-card">
          <div class="mastery-metric-num">${metrics.totalChapters}</div>
          <div class="mastery-metric-label">பருவப் பாடங்கள் (Total Chapters)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#10b981;">${metrics.completedCount}</div>
          <div class="mastery-metric-label">வாசித்து உணர்ந்தவை (${metrics.percentage}%)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#38bdf8;">${metrics.totalXp.toLocaleString()}</div>
          <div class="mastery-metric-label">தர்ம சாதனா புள்ளிகள் (Vedic XP)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:var(--gold-bright);">${metrics.unlockedBadges} / ${metrics.totalBadges}</div>
          <div class="mastery-metric-label">நிறைவுப் பதக்கங்கள் (Ashram Badges)</div>
        </div>
      </div>

      <!-- Books Mastery Cards Grid -->
      <div style="margin: 20px 0 12px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="color:#ffffff; font-size:1.15rem; font-weight:800; margin:0;">
          ${masteryTitle}
        </h3>
        <span style="font-size:0.8rem; color:#94a3b8;">ஒவ்வொரு நூலிலும் 7 அத்தியாயங்கள்</span>
      </div>

      <div class="mastery-books-grid">
  `;

  const bookBadges = {
    'narcheyal': '☀️ நற்செயல் கர்மவீரர் (Action Champion & 3 Ds)',
    'nalvazhi': '⭐ நற்பண்பு நேர்மையாளர் (Virtue & Truth Bearer)',
    'nanneri': '🏅 நன்னெறி சுடர் (Conduct Pillar)',
    'nallaram': '🛡️ நல்லறச் செம்மல் (Dharma Champion)',
    'narthunai': '🪔 நற்துணை யோகி (Divine Refuge)',
    'narchol': '🌸 நற்சொல் வள்ளல் (Sweet Word Master)',
    'narchinthanai': '⚛️ நற்சிந்தனை ஞானி (Wisdom Seeker)'
  };

  activeBooks.forEach((book, idx) => {
    const done = metrics.bookMetrics[book.id] || 0;
    const isMastered = (done === 7);
    const pct = Math.round((done / 7) * 100);

    let dotsHtml = '';
    for (let c = 1; c <= 7; c++) {
      const cDone = isBookChapterCompleted(grade, book.id, c);
      dotsHtml += `<span class="mastery-dot ${cDone ? 'done' : ''}" title="அத்தியாயம் ${c}: ${cDone ? 'நிறைவு பெற்றது' : 'படிக்க வேண்டியுள்ளது'}"></span>`;
    }

    const badgeName = bookBadges[book.id] || `${book.name} தேர்ச்சிப் பதக்கம்`;'''

if old_mastery in content:
    content = content.replace(old_mastery, new_mastery)
    print("SUCCESS: renderMasteryPanelHtml updated!")
else:
    print("ERROR: old_mastery not found!")

# 5. Update renderDiplomaPanelHtml
old_diploma = '''function renderDiplomaPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const studentName = localStorage.getItem('gkd_student_name') || 'மாணவர்';
  const todayStr = new Date().toLocaleDateString('ta-IN', { year: 'numeric', month: 'long', day: 'numeric' });
  const isPrimary = (grade <= 5);

  const diplomaBody = isPrimary ? `
    இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் தொடக்கப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>3 முதன்மை ஆசிரமப் பாடநூல்கள்</strong> (நற்செயல், நல்வழி, நற்துணை ஆகிய 21 அத்தியாயங்கள் — விளையாடிப் பயிலல், பகிர்தல், பெரியோர் பணிவு, இறைத் துதி, தத்துவ விரிவுரைகள் மற்றும் தினசரி சாதனா பயிற்சிகள்) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
  ` : `
    இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>7 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நல்வழி, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் ஆகிய 49 அத்தியாயங்கள், மூலப் பாடல்கள், தத்துவ விரிவுரைகள் மற்றும் தினசரி சாதனா பயிற்சிகள்) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
  `;

  return `
    <div class="diploma-outer-wrap">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
        <span style="color:#94a3b8; font-size:0.85rem;">தரம் ${grade} — 3 மாத காலப் பருவ நிறைவுச் சான்றிதழ்</span>
        <div style="display:flex; gap:8px;">
          <button type="button" class="sheet-btn" onclick="editStudentName()" style="font-size:0.82rem; padding:6px 14px;">
            ✍️ மாணவர் பெயர் மாற்றுக
          </button>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="printGradeDiploma()" style="font-size:0.82rem; padding:6px 16px;">
            🖨️ சான்றிதழ் அச்சிடுக / PDF சேமிக்க
          </button>
        </div>
      </div>

      <!-- Traditional Vedic Certificate -->
      <article class="diploma-certificate-shell" id="gradeDiplomaShell">
        <div class="diploma-top-emblem">ॐ</div>
        <div class="diploma-inst-name">குரு குல ஆசிரமம் • வித்யா குடீரம் பள்ளி</div>
        <div class="diploma-inst-sub">Guru Kula Desam — Modern Gurukulam Online Vedic Academy</div>

        <h1 class="diploma-cert-title">${isPrimary ? 'தொடக்கப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்' : 'பருவ நிறைவுப் பட்டயச் சான்றிதழ்'}</h1>
        <div class="diploma-citation-intro">${isPrimary ? 'Primary Diploma of Dharmic & Curricular Completion' : 'Diploma of Dharmic & Curricular Completion'}</div>'''

new_diploma = '''function renderDiplomaPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const studentName = localStorage.getItem('gkd_student_name') || 'மாணவர்';
  const todayStr = new Date().toLocaleDateString('ta-IN', { year: 'numeric', month: 'long', day: 'numeric' });

  let diplomaTitle = 'பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
  let diplomaIntro = 'Diploma of Dharmic & Curricular Completion';
  let diplomaBody = '';

  if (grade <= 2) {
    diplomaTitle = 'மழலைப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Infant Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> மழலைப் பருவப் பாடத்திட்டத்தில் உள்ள <strong>நற்செயல்</strong> ஆசிரமப் பாடநூல் (7 அத்தியாயங்கள் — விளையாடிப் பயிலல், பகிர்தல், உள்ளதைக் கொண்டு மகிழ்தல், காலையில் விழித்தல், தூய்மை, புன்னகைக் கண்ணியம் மற்றும் மூல ஏடுகள் பயிற்சி) அடங்கிய 3 மாத காலப் பருவப் பயில்வை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 4) {
    diplomaTitle = 'தொடக்கப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Primary Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் தொடக்கப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>2 முதன்மை ஆசிரமப் பாடநூல்கள்</strong> (நற்செயல், நற்பண்பு ஆகிய 14 அத்தியாயங்கள் — விளையாடிப் பயிலல், பகிர்தல், நற்பண்புகள், உண்மை பேசுதல், பெரியோர் பணிவு மற்றும் தினசரி சாதனா பயிற்சிகள்) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 8) {
    diplomaTitle = 'நடுநிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Middle School Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் நடுநிலைப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>5 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்செயல் ஆகிய 35 அத்தியாயங்கள் — தாய்-தந்தை வழிபாடு, ஜீவகாருண்யம், உண்மை நெறி, இறை பக்தி, 3 Ds வாழ்வியல் சாதனா) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 12) {
    diplomaTitle = 'உயர்நிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'High School Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் உயர்நிலைப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>6 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சொல், நற்செயல் ஆகிய 42 அத்தியாயங்கள் — அறநெறி, நல்லறம், வாய்மை, இறை சரணாகதி, நாவடக்கம், இனிய உரை, 3 Ds வாழ்வியல் சாதனா) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else {
    diplomaTitle = 'உயர்கல்விப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Higher Studies Vedic Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>உயர்கல்வி வித்யாபீடப்</strong> பாடத்திட்டத்தில் உள்ள <strong>7 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் ஆகிய 49 அத்தியாயங்கள் — வேத-நவீன அறிவியல் சங்கமம், குவாண்டம் இயற்பியல், வேதாந்தம், உபநிடதங்கள், தினசரி பஞ்ச மகா யாகங்கள் & 3 Ds) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  }

  return `
    <div class="diploma-outer-wrap">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
        <span style="color:#94a3b8; font-size:0.85rem;">தரம் ${grade} — 3 மாத காலப் பருவ நிறைவுச் சான்றிதழ்</span>
        <div style="display:flex; gap:8px;">
          <button type="button" class="sheet-btn" onclick="editStudentName()" style="font-size:0.82rem; padding:6px 14px;">
            ✍️ மாணவர் பெயர் மாற்றுக
          </button>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="printGradeDiploma()" style="font-size:0.82rem; padding:6px 16px;">
            🖨️ சான்றிதழ் அச்சிடுக / PDF சேமிக்க
          </button>
        </div>
      </div>

      <!-- Traditional Vedic Certificate -->
      <article class="diploma-certificate-shell" id="gradeDiplomaShell">
        <div class="diploma-top-emblem">ॐ</div>
        <div class="diploma-inst-name">குரு குல ஆசிரமம் • வித்யா குடீரம் பள்ளி</div>
        <div class="diploma-inst-sub">Guru Kula Desam — Modern Gurukulam Online Vedic Academy</div>

        <h1 class="diploma-cert-title">${diplomaTitle}</h1>
        <div class="diploma-citation-intro">${diplomaIntro}</div>'''

if old_diploma in content:
    content = content.replace(old_diploma, new_diploma)
    print("SUCCESS: renderDiplomaPanelHtml updated!")
else:
    print("ERROR: old_diploma not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("File updated successfully.")
