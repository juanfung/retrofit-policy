---
title: Hedonic models for retrofit policy
author: Juan Fung
date: May 4, 2020
fontsize: 12pt
---

I am thinking of two different models.

# Model 1: Property level

Consider the following hedonic diff-in-diff equation. 

\begin{align}
p\sb{ijt} = \lambda\sb{t} + \alpha\sb{j} + z\sb{jt} \beta + x\sb{ijt}
\delta\sb{jt} + v\sb{jt} + \epsilon\sb{ijt} \label{eq:main}
\end{align}

where $i$ is the index for the unit of observation (in this case, the property),
$j$ is the index for the group, and $t$ is the index for time. The policy
variable is $z\sb{jt}$ and so the parameter of interest is $\beta$. The property
characteristics are in the vector $x\sb{ijt}$. The parameters $\lambda\sb{t}$
and $\alpha\sb{j}$ are vectors of time and group fixed effects,
respectively. Finally, $v\sb{jt}$ and $\epsilon\sb{ijt}$ are idiosyncratic
errors.

If $j=\{\mbox{Control, Treatment}\}$ and $t=\{1,2\}$, then we have the canonical
two-period, two-group diff-in-diff and
$z\sb{jt}=1$ if $j=$ Treatment and $t=2$.

The model in Eq. \eqref{eq:main} is general enough to accommodate more groups
and more periods (and indeed multiple treatments at multiple periods). We can
discuss this at a later stage. For now, let's focus on the canonical model.

We have two possible experiments (i.e., two possible treatments for the
canonical model):

1. Being designated as "hazardous"
2. Being in the "neighborhood of a hazardous building"

## Experimental design 1

Let's use the soft-story ordinance in San Francisco as an example. In the first
experiment, $j=$ Treatment if property $i$ is a soft-story home built before
1978 (i.e., it is on the list of properties to be retrofitted).

The control group could be a property $i$ that satisfies: 

- a soft-story home built on or after 1978
- a *non* soft-story home built before 1978
- a newer home, assumed built to current code (let's say 2012 since FEMA P-807
  was published in 2012; we can look into this later)

Suppose we could identify soft-story homes built prior to 1978 *in another
city*, then we could potentially have a "triple difference" design. This might
work with the way different cities rolled out their ordinances (e.g., Los
Angeles in 2015).
  
As we discussed, the main problem with this experiment is the lack of data on
prices in both time periods. If we extend the analysis to multiple time perios,
it's possible we may observe some homes with repeat sales but this is likely to
be a small subset of homes. An alternative to price is assessed value; while
imperfect, it is available annually. 

**Question**: Do you have any thoughts on how to address the data issue?

## Experimental design 2

Now consider the second experiment. Let $i\sp{*}$ denote a soft-story home built
before 1978. In this case a property $i$ is in the treatment group if it is in
the neighborhood of $i\sp{*}$. How do we define neighborhood? 

- Contiguity (e.g., binary, rook, queen). In essence, look at immediate
  neighbors of $i\sp{*}$, homes across from $i\sp{*}$, and homes diagonal from
  $i\sp{*}$.
- Distance. In essence, any home within some threshold distance of
  $i\sp{*}$. How to pick the threshold??
- $k$-Nearest Neighbors. In essence, pick the $k$ closest neighbors in terms of
  distance.

Moreover, we can also assume that a soft-story home built before 1978 is in the
neighborhood of itself.

In this case, the treatment is supposed to reflect that a home is in a
"hazardous neighborhood." This is a strong assumption. To what extent do we
expect that a buyer for $i$ is aware of $i\sp{*}$ being hazardous? To what
extent do they care? 

It would be interesting to explore the data to see if there are "clusters" of
hazardous homes. In this case, it may be more plausible that the area is
"hazardous."

On the other hand, this experiment has the potential to yield more observations,
since we may observe more homes in both periods. I'm still not sure there will
be enough homes selling in both periods, but perhaps this could work with
multiple periods.

**Question**: Do you have any thoughts on how to address the data issue?

## Threats to validity

The main threat to validity (that is, to the claim that the treatment is
quasi-random) is *selection*. This means that it's possible owners who do not
want to retrofit their homes sell their homes before they have to retrofit them
(these sellers select out of treatment) and that buyers who value safe homes are
willing to pay for and retrofit a hazardous home (these buyers select into
treatment). In this case, their is an unobserved variable that affects the
selection into or out of treatment but also affects the *price*. This causes the
policy effect to be endogenous.

The issue is a bit more complicated than what I've written and will require
careful consideration. 

**Remark**: This is something I want you to start thinking (and writing) about.


# Model 2: County level

For simplicity, if we assume the unit of observation is the group $j$ itself
(e.g., the city or the county), then we can drop the $i$ index in
Eq. \eqref{eq:main}:

\begin{align}
p\sb{jt} = \lambda\sb{t} + \alpha\sb{j} + z\sb{jt} \beta + \epsilon\sb{jt} \label{eq:county}
\end{align}

where now $j$ is the index for the county. In the canonical model, we have a
treatment county and a control county and $t=\{1,2\}$. We could also add
time-varying characteristics $x_{jt}$ for county $j$.

In this case, we don't have to worry about the data limitations! This is the
obvious advantage. Of course, the major drawback is that this is capturing
effects at the aggregate level. The price $p\sb{jt}$ is some aggregat measure of
property price (e.g., mean, median).



## Experimental design

In this setting, $z\sb{jt}=1$ if a city/county passed a retrofit ordinance at
time $t$. This model can easily be extended to multiple groups and time periods.

**Remark**: I think this may be the easiest place to start.

There are two options for the model in Eq. \eqref{eq:county}:

1. A diff-in-diff for treatment vs control county (e.g., SF vs Oakland), which
   is what Eq. \eqref{eq:county} represents.
2. Synthetic control: one treatment group, many control counties that contribute
   to a single "synthetic" control. This is an extension of diff-in-diff, but
   the model is actually different than Eq. \eqref{eq:county}.
