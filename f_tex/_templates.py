class Templates:
    """
    ============================================================================
     Static .tex Source Builders.
    ============================================================================
    """

    @staticmethod
    def session_summary(project_name: str,
                        date: str,
                        project_path: str,
                        body: str) -> str:
        """
        ========================================================================
         Build a Session-Summary .tex Source.
         body is raw LaTeX inserted after the standard title block.
         Follows Drive 'For_Session_Summary.md' conventions:
         orange accent, fancyhdr header, \\unchecked command available.
        ========================================================================
        """
        return (_SESSION_SUMMARY
                .replace('__PROJECT_NAME__', project_name)
                .replace('__DATE__', date)
                .replace('__PROJECT_PATH__', project_path)
                .replace('__BODY__', body))


# ============================================================================
# Session-summary LaTeX template. Placeholders are __NAME__ style so curly
# braces in the LaTeX body do not need escaping.
# ============================================================================
_SESSION_SUMMARY = r"""\documentclass[11pt, a4paper]{article}

% -- Packages -------------------------------------------------------
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=2.5cm]{geometry}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{listings}
\usepackage{amssymb}

% -- Colours --------------------------------------------------------
\definecolor{accent}{HTML}{E65100}
\definecolor{linkblue}{HTML}{1565C0}
\definecolor{codebg}{HTML}{F5F5F5}
\definecolor{rulegray}{HTML}{BDBDBD}

% -- Hyperlinks -----------------------------------------------------
\hypersetup{
    colorlinks=true, linkcolor=accent, urlcolor=linkblue,
}

% -- Section styling ------------------------------------------------
\titleformat{\section}
    {\Large\bfseries\color{accent}}{\thesection}{1em}{}
    [\vspace{-0.4em}\textcolor{rulegray}{\rule{\textwidth}{0.4pt}}]
\titleformat{\subsection}
    {\large\bfseries}{}{0em}{}

% -- Header / footer ------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\lhead{\small\textcolor{gray}{__PROJECT_NAME__}}
\rhead{\small\textcolor{gray}{__DATE__}}
\cfoot{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}

% -- Code listings --------------------------------------------------
\lstset{
    basicstyle=\ttfamily\small,
    backgroundcolor=\color{codebg},
    frame=single, rulecolor=\color{rulegray},
    breaklines=true, columns=fullflexible, keepspaces=true,
    xleftmargin=1em, framexleftmargin=0.5em,
    aboveskip=1em, belowskip=1em,
}

% -- Checkbox -------------------------------------------------------
\newcommand{\unchecked}{$\square$\;}

\begin{document}

% -- Title block ----------------------------------------------------
\begin{center}
    {\Huge\bfseries\color{accent} __PROJECT_NAME__}\\[0.6em]
    {\Large Session Summary}\\[1em]
    {\large\textbf{Date:} __DATE__ \qquad
     \textbf{Project:} \texttt{__PROJECT_PATH__}}
\end{center}
\vspace{1.5em}

__BODY__

\vfill
\begin{center}
\textcolor{rulegray}{\rule{0.5\textwidth}{0.3pt}}\\[0.4em]
\small\textcolor{gray}{Generated __DATE__ --- __PROJECT_NAME__}
\end{center}

\end{document}
"""
