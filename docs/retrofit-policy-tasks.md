---
title: Retrofit policy tasks
author: Juan Fung
date: May 11, 2020
fontsize: 12pt
---

Since I may be out for a few weeks, I wanted to lay out a plan for the near term
(roughly the next two months).  Just to make sure we are on the same page, for
now we are focusing on the designation for retrofit as the treatment (rather
than the retrofit itself).

Priority tasks (in no particular order; may be done in parallel)

1. Begin thinking about and addressing exogeneity and potential threats to
   validity. This is not an exhaustive list; please consult Parmeter and Pope's
   chapter on "Quasi-Experiments and Hedonic Property Price Methods."
      - I'm assuming treatment is exogenous, in the sense that the designation
        of buildings to be retrofitted was not driven by the building owners
        themselves, or that they were involved in crafting the ordinance; highly
        unlikely but any evidence you can find will support.
      - What we need to careful with is selection into or out of treatment; eg,
        with several years lead time before the ordinance, it's possible home
        owners saw the designation coming and sold their house in anticipation
        of the ordinance. This is an example of selecting out of
        treatment. 
2. Work on Model 2: city/county level.
      - Begin collecting data for a two-group diff-in-diff (e.g., SF vs
        Oakland; SF vs LA may work too given LA's ordinance was in 2015)
      - Another possibility is to compare city with a mandatory ordinance (eg,
        SF) to a city with a voluntary ordinance
      - Initial estimates for two-group diff-in-diff
      - May not yield anything meaningful, but an easy place to start
3. Work on Model 1: parcel-level
      - Experiment 1 vs Experiment 2: Experiment 2 is an easier place to start
        and potentially the treatment group is larger; but plausibility of
        treatment for neighbors is a question.
      - Sale price data vs tax assessor data: sale price data is ideal, but it
        is unlikely we will observe many repeat sales (esp for
        treatment). Assessessments are done every year. If we can do both, we
        should compare results; however, let's start with assessments
      - The most important question: What are the controls? We may be able to
        use assessor/permit data to identify appropriate controls (based on year
        built and construction type). 
      - We've been thinking about treatment locally; what if we consider any
        home in the state of CA that has received the treatment? eg, homes in SF
        receive treatment in 2013; homes in LA in 2015; homes in Santa Monica
        in 2019.  Based on your Table 2 on soft-story ordinances, this is 25,458
        homes that are treated across the entire state. This strategy could
        potentially increase the sample size for the treatment group if we
        observe enough homes with repeat sales.
      - So let's proceed as follows: 
          - Experiment 1 using assessor data
          - If Experiment 1 using assessor data does not yield meaningful
            results, let's consider Experiment 2 with assessor data
          - After that, we can consider Experiment 2 with sale price data
4. Compile a literature review
      - This will include a **brief** review of causal hedonic methods
      - Literature on quantifying impacts of retrofits (should be small)
      - Related literature on quantifying impacts of (seismic?) mitigation
        policies
      - May be a separete section, but somewhat brief background/context for
        retrofit ordinance under study (eg, in SF); essentially a narrative from
        the documents you've put together on short story in CA and short story
        in SF
5. What do we want to approach Ruchi about?
      - Collaboration / feedback on Model 1 is the obvious candidate
      - Let's think about some precise questions or issues we can bring to her
      - I think she has a paper on using assessments vs sales prices
