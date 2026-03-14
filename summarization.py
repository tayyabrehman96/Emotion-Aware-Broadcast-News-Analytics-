from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def split_text_into_chunks(text, max_chunk_size=400):
    """
    Split text into chunks smaller than max_chunk_size tokens to avoid token limit issues.
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_chunk_size):
        chunks.append(" ".join(words[i:i + max_chunk_size]))
    
    return chunks

def summarize_text(text, max_length_percentage=0.4):
    """
    Summarizes the text such that the final summary is approximately 40% of the original text length.
    """
    # Split the original text into chunks
    chunks = split_text_into_chunks(text)
    
    # Summarize each chunk and collect results
    summaries = []
    
    for chunk in chunks:
        # Calculate word count of chunk
        chunk_word_count = len(chunk.split())
        target_summary_length = int(chunk_word_count * max_length_percentage)
        min_summary_length = max(50, int(target_summary_length * 0.7))  # Ensure minimum length for coherence

        # Ensure that min_length is never greater than max_length
        if min_summary_length > target_summary_length:
            min_summary_length = max(1, target_summary_length - 10)  # Adjust to avoid errors
        
        # Summarize the chunk
        summary = summarizer(
            chunk, 
            max_length=target_summary_length, 
            min_length=min_summary_length, 
            do_sample=False
        )
        summaries.append(summary[0]['summary_text'])
    
    # Combine all summaries
    combined_summary = " ".join(summaries)
    
    return combined_summary


# Sample text to summarize
text = """Prime Minister Shahbha Sharif is visiting Karachi for two days. He emphasized the federal government's commitment to supporting Sindh and inquired about the progress of radlarif efforts. He also addressed the international Food and Agriculture Exhibition. As you all know, Pakistan is an agrarian economy and more than 60% of our population reside in rural areas. We need to really further strengthen and augment our agricultural produce at the moment. Chairman TDAP, as mentioned this morning that our exports have increased in agriculture sector by $3 billion during the last financial year, we have fixed a target of an additional $7 billion for this year. That is a quantum jump and it requires huge efforts. Pakistan needs modern technology. Pakistan needs modern techniques and best practices to boost our agriculture production and then have value added products for our exports in that China can be our best partner to help us achieve our target in this field. The prime minister set a target of $7 billion for agriculture exports and praised Arshad Nadeem's olympic gold medal achievement. Meanwhile, Doctor Imam Salah bin Mohammed al Budir of Masjid al Nabri met with Pakistan's army chief General Asim Munir, highlighting Pakistan's significant role in the muslim world. Meanwhile, the Bloach Yakiti committee, sea and government reached an agreement ending eleven day sit in Balochistan with a committee to oversee implementation of agreed upon points. Furthermore, US Ambassador Donald Bloom praised Pakistans decision to extend the stay of registered afghan refugees by a year, citing the countrys long history of 
hosting afghan refugees. Lastly, Pakistans Foreign office denied reports of supplying Shaheen ballistic missiles to Iran, calling them baseless, and emphasized Pakistans participation in regional and international matters. The deputy prime minister expressed an unequivocal condemnation of israeli brutalities and warmongering and its actions that have caused irreparable damage to the already fragile and volatile Middle east. He also called for preventing further escalation of tensions and violence in the region. The deputy prime minister and foreign minister called for enhanced humanitarian assistance for the Palestinians in Gaza, for opening all access points of supply to Gaza and allowing all UN and international agencies, including UNRWA, to operate fully in Gaza. Deputy prime minister also underlined the need for establishment of an international judicial mechanism which would seek restitution, damages and satisfaction from Israel for its crimes against humanity, war crimes and genocide in Gaza and hold those accountable for their crimes. Philip Lazzarni, the head of the UN agency for palestinian refugees, is sounding the alarm about the war in Gaza. He said it's not just the buildings and infrastructure that are being destroyed, but the entire community is being torn apart. He posted on X that the social fabric and close tent relationships in Gaza are being shredded. Lizarani also emphasized that once a ceasefire is in place, it's just as urgent to start rebuilding these community ties. Hamas armed wing, the Qassam brigades, has announced that its fighters targeted a building in Dital al Sultan area of western Rafah where israeli soldiers were stationed. They claim to have hit nine soldiers with two TBG shells, either killing or injuring them, according to their statement. They also observe israeli army helicopters arriving to evacuate the dead and wounded. French President Emmanuel Macaron is backing the push for a ceasefire in Gaza, saying the war needs to stop. In a post on next, he expressed Frances full support for the efforts 
by the us, egyptian and qatari mediators to broker a deal. In the ceasefire talk set for next week, which Israel has agreed to join, Macron stressed that a ceasefire is vital for the people, for Gaza, for the hostages, and for the stability for the region. The ABC network has confirmed that both presidential candidates Donald Trump and Kamala Harris will attend a debate on the 10 September 2024. Trump, the republican nominee, mentioned during a news conference in Florida that he wants additional debates on September 4 and 25th, but he didnt provide details and its unclear if Harris team has agreed. We have somebody that hasn't received one vote for president and she's running and that's fine with me, but we were given Joe Biden and now we're given somebody else. And I think, frankly, I'd rather be running against somebody else. But that was their choice. They decided to do that because Kamala's record is horrible. She's a radical left person at a level that nobody's seen. She picked a radical left man that is, he's got things done that he, he has positions that are just not, it's not even possible to believe that they exist. He's going for things that nobody's ever 
even heard of. Heavy into the transgender world, heavy into lots of different worlds, having to do with safety. He doesn't want to have borders. He 
doesn't want to have walls. He doesn't want to have any form of safety for our country. He doesn't mind people coming in from prisons and neither does she, I guess, because she's not, she couldn't care less. She's the border czar, by the way. She was the border czar 100%. And all of a sudden, for the last few weeks, she's not the border czar anymore. Like nobody ever said it. This announcement follows Harris recent rise in the race, which has shaken up the election her entry into the race after replacing President Biden as democratic candidates has energized Democrats, drawing large crowds and significant fundraising. This has forced Trumps campaign to readjust their strategy. Microsoft researchers report that groups linked to the Irani government are interfering with us elections through disinformation campaigns and hacking. One group, Storm 2035, is creating fake news sites targeting both rebels and conservatives, spreading divisive content on topics like the presidential candidates, lgbt rights and Israel Hamas conflict. Theyre using AI to plagiarize us content and increase their visibility online. Another group, Zafeed Flood, started operations in March, impersonating activist groups to sow doubt about election integrity and encourage violence against political figures. Vice President Kamala Harris is now the favorite to win the presidential election, according to bookmarkers. Over the past two weeks, shes closed in on and slightly overtaken Trump in the betting markets. On poly market, Harris has a 49% chance of winning compared to Trumps 48%. This is a big change from two weeks ago, when Trump had led by a wide margin on the pericult. Harris has even stronger odds, with a 57% chance of winning. Her choice of Minnesota governor Tim Walz as a running mate seems to have boosted her lead further."""

# Summarize the text
summary = summarize_text(text)
print("Summarized Text:\n", summary)


