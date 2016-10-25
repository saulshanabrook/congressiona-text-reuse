Modeling text re-use in congressional legislation

Recent work in political science suggests that U.S. Congressional bills, traditionally imagined to be written by a single sponsor, sometimes contain bits and pieces of other legislation.

For our project, we would like to identify and model this “text reuse” in U.S. Congressional bills. If parts of bills are in fact reassembled from others, then better understanding of this process might help explain what legislative ideas become law.

Analyzing text re-use in congressional legislation offers a chance to enhance two different strains of applied machine learning and political science research: topic modeling and ideal point analysis. We have discussed topic modeling in 697. In ideal point analysis, the goal is to place political actors into some mathematical space, which models and predicts their behavior. The method has been used in many contexts, such as predicting votes on the supreme court [3].

Recently, some researchers have begun to join these two strangs of research. David Blei and Sean M. Gerrish have explored improving such point estimates with textual topic models or issue-focused topic models [1]. Meanwhile, David Bamman and Noah Smith have explored learning point estimates for propositions like (Barack Obama, is, a socialist) [2]. Modeling textual borrowing might offer another way to join these two strands of research. Given that majority parties often decide what votes are cast [4], we are particularly interested if textual borrowing offers out-of-power parties a chance to present ideas to congress.

We will be using a corpus of 97,221 U.S. congressional bills, assembled by Prof. Brendan O’Connor and one of his former students, Matt Denny. The first phase of our project will use text shingling [5] to efficiently find near duplicates in congressional bills. We have already implemented shingling and are working to adapt methods that run on small toy corpora to run on the entire large corpus.

Notes

[1] http://www.cs.columbia.edu/~blei/papers/GerrishBlei2011.pdf
[2] http://www.aclweb.org/anthology/D15-1008
[3] http://mqscores.berkeley.edu/media/pa02.pdf
[4] http://faculty.mwsu.edu/politicalscience/jeremy.duff/Research%20Papers/Congress/campbellcoxmccubbins.pdf
[5] nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html