#lang racket

(require racket/pretty)
(require racket/list)
(require racket/match)
(require json)
(require racket/math)
(require racket/format)
(require racket/string)


(define (parse-kicad-pcb fname)
    (let ([sexp (call-with-input-file fname
            (lambda (in)
                (read in)))])
        sexp))

(define (kicad->area sexp)
  (match sexp 
       [`(kicad_pcb 
          ,(not `(general ,_ ...)) ...
          (general 
           ,_ ...
           (area ,x1 ,y1 ,x2 ,y2)
           ,_ ...)
          ,_ ...)
         (list x1 y1 x2 y2)]
        [_ (list 0 0 0 0)]))

;; module has shape and pads, pad belong to 0 or 1 netlist
(define (module-clause->module module-clause)
  (match module-clause
       [`(module ,name
                 ;; CAUTION there might be a "locked" item
                 ,_ ...
                 (layer ,layer)
                 ,_ ...
                 ;; FIXME z?
                 (at ,x ,y ,z ...)
                 ,(not `(pad ,_ ...)) ...
                 (pad ,_
                      ,type
                      ,shape
                      ;; FIXME padz
                      (at ,padx ,pady ,padz ...)
                      ,_ ...
                      (layers ,layers ...)
                      ;; there might be a net OR NOT
                      ,(not `(net ,_ ...)) ...
                      (net ,netId ,_) ...
                      )
                 ;; FIXME some modules might not have pads
                 ...
                 ,_ ...
                 )
         ;; module
         (hash 'x x
               'y y
               'pads (for/list ([t type]
                               [s shape]
                               [x padx]
                               [y pady]
                               [net netId]
                                [l layers])
                               (hash 'type (symbol->string t)
                                     'shape (symbol->string s)
                                     'x x
                                     'y y
                                     'net (if (empty? net) null (first net))
                                     'layers (begin 
                                                (let ([res '()])
                                                  (when (or (member 'F.Cu l)
                                                            (member '*.Cu l))
                                                        (set! res (append res '("F"))))
                                                      (when (or (member 'B.Cu l)
                                                                (member '*.Cu l))
                                                            (set! res (append res '("B"))))
                                                      res)

                                                      ))
                              ))
         ]))

(define (kicad->modules sexp)
  (define clauses (match sexp
       [`(kicad_pcb
          ,clauses ...)
         clauses]))
  (define module-clauses (filter (lambda (x)
              (match x
                     [`(module ,_ ...) #t]
                     [else #f]))
        clauses))
  (define modules
      (for/list ([c module-clauses]
          [i (in-naturals)])
         (module-clause->module c)))
  modules
  )

(define (kicad-file->json in-fname out-fname)
  (define sexp (parse-kicad-pcb in-fname))
  ;; clauses
  (define clauses (match sexp
       [`(kicad_pcb
          ,clauses ...)
         clauses]))
  (define area (kicad->area sexp))
  (define modules (kicad->modules sexp))
  (call-with-output-file out-fname
                       #:exists 'replace
                     (lambda (out)
                       (write-json (hash 'modules modules
                                         'area area)
                                   out))))



(define verbose-mode (make-parameter #f))
(define profiling-on (make-parameter #f))
(define optimize-level (make-parameter 0))
(define link-flags (make-parameter null))
 
(define file-to-compile
  (command-line
   #:program "converter"
   #:args (in-fname out-fname) ; expect one command-line argument: <filename>
   ; return the argument as a filename to compile
   (list in-fname out-fname)))

;; (kicad-file->json "./benchmarks/cantact.kicad_pcb" "out1.json")
(displayln (~a "Running: IN: " (first file-to-compile) " OUT: " (second file-to-compile)))
(kicad-file->json (first file-to-compile) (second file-to-compile))