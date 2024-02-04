
'use client'
import Image from "next/image"
import styles from './styles.module.css'
import { cn } from "@/lib/utils"
import { useState } from "react"


const leftLines = [
  "Lorem Ipsum is simply dummy text of the",
  "printing and typesetting industry. Lorem Ipsum has been the industry's standard ",
  "dummy text ever since the 1500s, when",
  "an unknown printer took a galley of type and scrambled it to make a type specimen book.",
  "It has survived not only five centuries, but also the leap into electronic typesetting,",
  "remaining essentially unchanged. It was popularised",
  "in the 1960s with the release of Letraset sheets containing Lorem Ipsum",
  "passages, and more recently with desktop publishing software like Aldus",
  "PageMaker including versions of Lorem Ipsum."
]

const rightLines = leftLines.slice().reverse()

export default function Home() {
  const [highlightedRow, setHighlightedRow] = useState<number>(-1)
  const [submittedText, setSubmittedText] = useState<string | null>(null)
  const [textBoxContent, setTextBoxContent] = useState<string>('')

  const dynamicRows = { gridTemplateRows: `repeat(${rightLines.length}, minmax(0, 1fr))` }

  const textUploader = <div className={cn('flex flex-col items-center justify-center h-full')}>
    <textarea
      id="text-upload"
      value={textBoxContent}
      onChange={(e)=>{e.preventDefault(); setTextBoxContent(e.target.value)}}
      className={cn('w-1/2 h-3/4')}
    />
    <div className={cn('h-4')} />
    <button onClick={()=>setSubmittedText(textBoxContent)} className={cn('bg-purple-300 p-2 rounded-md')}>Submit</button>
  </div>

  const translationDisplay = <div style={dynamicRows} className={cn('grid grid-cols-2 grid-flow-col gap-x-4 gap-y-1')}>
    {leftLines.map((line, i)=>
      <div
        key={i}
        onMouseEnter={(e)=>{e.preventDefault(); setHighlightedRow(i)}}
        onMouseLeave={(e)=>{e.preventDefault(); setHighlightedRow(-1)}}
        className={cn('p-2 bg-red-300', highlightedRow === i ? 'bg-red-700' : '')}
      >
        {line}
      </div>)
    }
    {rightLines.map((line, i)=>
      <div
        key={i}
        onMouseEnter={(e)=>{e.preventDefault(); setHighlightedRow(i)}}
        onMouseLeave={(e)=>{e.preventDefault(); setHighlightedRow(-1)}}
        className={cn('p-2 bg-blue-300', highlightedRow === i ? 'bg-blue-700' : '')}
      >
        {line}
      </div>)
    }
  </div>
  return (
    <div className={cn("flex flex-col items-center justify-center bg-green-300 h-full p-12")}>
      <div className={cn('text-lg bg-slate-900 w-full h-full max-w-[800px] overflow-auto p-4')}>
        {submittedText !== null ? translationDisplay : textUploader}
        {/* <div className={cn('text-white')}>{submittedText}</div> */}
      </div>
    </div>
  )
}
