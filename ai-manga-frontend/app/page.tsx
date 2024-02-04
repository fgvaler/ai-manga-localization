
'use client'
// import Image from "next/image"
// import styles from './styles.module.css'
import { cn } from "@/lib/utils"
import { useState } from "react"

export default function Home() {
  const [highlightedRow, setHighlightedRow] = useState<number>(-1)
  const [textBoxContent, setTextBoxContent] = useState<string>('')

  const [translatedText, setTranslatedText] = useState<string[] | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  const origTextLines = textBoxContent.split('\n').map(line=>line.trim()).filter(line=>line.length > 0)
  const numLines = Math.min(origTextLines.length, translatedText ? translatedText.length : 0)
  const origTextFirstN = origTextLines.slice(0, numLines)
  const translatedTextFirstN = translatedText ? translatedText.slice(0, numLines) : []

  const fetchTranslation = async (text: string) => {
    setLoading(true)
    const res = await fetch('http://localhost:8000/translate',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'text': text
      })
    })
    // const data = await res.json()
    // setTranslatedText(data['data'])


    const reader = res.body?.getReader();
    if (!reader) { // make typescript happy
      return;
    }

    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      // console.log([done, value, reader])
      if (done) break;
      
      const decodedValue = decoder.decode(value);
      
      const message = JSON.parse(decodedValue);
      setTranslatedText((prevArr) => prevArr ? prevArr.concat(message.data) : [message.data]);
    }
  }

  const dynamicRows = translatedText?{ gridTemplateRows: `repeat(${numLines}, minmax(0, 1fr))` }:{}

  const textUploader = <div className={cn('flex flex-col items-center justify-center h-full')}>
    <textarea
      id="text-upload"
      value={textBoxContent}
      onChange={(e)=>{e.preventDefault(); setTextBoxContent(e.target.value)}}
      className={cn('w-1/2 h-3/4')}
    />
    <div className={cn('h-4')} />
    {
      loading
        ?
      <div className={cn('text-purple-300 p-2 rounded-md')}>Loading...</div>
        :
      <button onClick={()=>fetchTranslation(textBoxContent)} className={cn('bg-purple-300 p-2 rounded-md')}>
        Submit
      </button>
    }
  </div>

  const translationDisplay = translatedText ? <div style={dynamicRows} className={cn('grid grid-cols-2 grid-flow-col gap-x-4 gap-y-1')}>
    {origTextFirstN.map((line, i)=>
      <div
        key={i}
        onMouseEnter={(e)=>{e.preventDefault(); setHighlightedRow(i)}}
        onMouseLeave={(e)=>{e.preventDefault(); setHighlightedRow(-1)}}
        className={cn('p-2 bg-red-300', highlightedRow === i ? 'bg-red-700' : '')}
      >
        {line}
      </div>)
    }
    {translatedTextFirstN.map((line, i)=>
      <div
        key={i}
        onMouseEnter={(e)=>{e.preventDefault(); setHighlightedRow(i)}}
        onMouseLeave={(e)=>{e.preventDefault(); setHighlightedRow(-1)}}
        className={cn('p-2 bg-blue-300', highlightedRow === i ? 'bg-blue-700' : '')}
      >
        {line}
      </div>)
    }
  </div> : null

  return (
    <div className={cn("flex flex-col items-center justify-center bg-green-300 h-full p-12")}>
      <div className={cn('text-lg bg-slate-900 w-full h-full max-w-[800px] overflow-auto p-4')}>
        {translatedText !== null ? translationDisplay : textUploader}
      </div>
    </div>
  )
}
