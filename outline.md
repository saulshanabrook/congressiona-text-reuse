Modeling text re-use in congressional legislation

Recent work in political science (Cite: Wilkerson) suggests that U.S. Congressional bills, traditionally imagined to be written by a single sponsor, sometimes contain bits and pieces of other legislation. For instance, HR 3590, the Affordable Care Act, began as a measure promoting veteran home ownership. (Cite: Wilkerson) As political scientists write: the linear “legislative process” perspective taught in civics courses fails to capture the twists and turns of many policy proposals in Congress.

For our project, we would like to identify and model this “text reuse” in U.S. Congressional bills. If parts of bills are in fact reassembled from others, then better understanding of this process might help explain what policy ideas succeed or fail in the legislature. We still need to do initial exploratory analysis to better understand what modeling might be appropriate, but we are intrigued by the idea of using methods from genetics to study the the U.S. congress — as well as using graphical models to better understand the functioning of the legislature.

We will be using a corpus of 97,221 U.S. congressional bills, assembled by Prof. Brendan O’Connor and one of his former students, Matt Denny. The first phase of our project will use text shingling (Cite: Stanford IR) to efficiently find near duplicates in congressional bills. We have already implemented shingling and are working to adapt our methods to run on the whole corpus.

Analyzing text re-use offers a chance to enhance the ideal point estimates common in political science.  Roughly, in ideal point analysis, the goal is to place political actors into some mathematical space, which models and predicts their behavior. Recently, machine learning researchers like David Blei (Cite: Gerrish Blei) have explored improving such point estimates with textual topic models or issue-focused topic models (Cite: Gerrish Blei). Natural language processing researchers like David Bamman have explored learning point estimates for propositions like (Barack Obama, is, a socialist). Textual borrowing might offer a way to enhance such models. Given that majority parties often decide what votes are cast (Cite: setting the agenda), we are particularly interested if textual borrowing offers out-of-power parties a chance to present ideas to the chamber.


Notes

https://polisci.osu.edu/sites/polisci.osu.edu/files/clinton_OSUIdealPointPrimer.pdf
