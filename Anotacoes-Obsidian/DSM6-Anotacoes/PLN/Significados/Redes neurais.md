## O que é uma rede neural?

Uma rede neural é um modelo de aprendizado de máquina que empilha neurônios simples em camadas e aprende pesos e vieses que reconhecem padrões a partir dos dados para mapear entradas para saídas.

Redes neurais estão entre os algoritmos mais influentes no [aprendizado de máquina](https://www.ibm.com/br-pt/think/topics/machine-learning) e na [inteligência artificial (IA)](https://www.ibm.com/br-pt/think/topics/artificial-intelligence). Elas sustentam avanços em [computer vision](https://www.ibm.com/br-pt/think/topics/computer-vision), [processamento de linguagem natural](https://www.ibm.com/br-pt/think/topics/natural-language-processing), [reconhecimento de fala](https://www.ibm.com/br-pt/think/topics/speech-recognition) e inúmeras aplicações do mundo real, que vão desde forecasting até reconhecimento facial. Enquanto as redes neurais profundas (DNNs) de hoje alimentam sistemas tão complexos quanto [transformadores](https://www.ibm.com/br-pt/think/topics/transformer-model) e [redes neurais convolucionais (CNNs),](https://www.ibm.com/br-pt/think/topics/convolutional-neural-networks) as origens das redes neurais remontam a modelos simples como a regressão linear e como o cérebro humano digere, processa e decide sobre as informações apresentadas a ele.
## Como funcionam as redes neurais?

Em um nível elevado, a inspiração para as redes neurais vem dos neurônios biológicos do cérebro humano, que se comunicam por meio de sinais elétricos. Em 1943, Warren McCulloch e Walter Pitts propuseram o primeiro modelo matemático de um neurônio, mostrando que unidades simples poderiam realizar o cálculo de uma função. Mais tarde, em 1958, Frank Rosenblatt introduziu o perceptron, um algoritmo projetado para realizar reconhecimento de padrões. O perceptron é o antecessor histórico das redes atuais: essencialmente um modelo linear com uma saída restrita. Na seção a seguir, nos aprofundaremos em como as redes neurais pedem inspiração nos cérebros humanos para tomar decisões e reconhecer padrões.  

Uma rede neural pode ser compreendida por meio de um exemplo simples: detecção de spam. Um e-mail é alimentado na rede, e funcionalidades como palavras ou frases como "prêmio", "dinheiro", "prezado" ou "ganhar" são usados como entradas. Os neurônios iniciais na rede processam a importância de cada sinal, enquanto as camadas posteriores combinam essas informações em pistas de nível superior que capturam contexto e tom. A camada final, então, calcula uma probabilidade de o e-mail ser spam e, se essa probabilidade for alta o suficiente, o e-mail será sinalizado. Em essência, a rede aprende a transformar funcionalidades brutas em padrões significativos e usá-los para fazer previsões.

Esse processo é alimentado por dois conceitos fundamentais: pesos e vieses. Os pesos atuam como mostradores que controlam a força com que cada funcionalidade de entrada influencia a decisão; uma palavra como "prêmio" pode receber mais peso do que uma palavra comum como "olá". Vieses são valores embutidos que mudam o limite de decisão, permitindo que um neurônio seja ativado mesmo que as entradas em si sejam fracas. Juntos, esses [parâmetros do modelo](https://www.ibm.com/br-pt/think/topics/model-parameters) determinam como cada neurônio contribui para a computação geral. Ao ajustar esses valores durante o treinamento, a rede aprende gradualmente a fazer previsões precisas — neste caso, se um e-mail é spam ou não.

De maneira matemática, uma rede neural aprende uma função  f(X)  mapeando um vetor de entrada  X=(x1,x2,x3...)  para prever uma resposta  Y.  O que distingue as redes neurais de outros algoritmos tradicionais de aprendizado de máquina é sua estrutura em camadas e sua capacidade de realizar transformação não linear.  

Uma rede neural é composta por:

- **Camada de entrada**: contém as funcionalidades brutas  (X1,X2,X3,..) .  
      
    
- **Camadas ocultas**: consistem em neurônios artificiais (ou nós) que transformam entradas em novas representações. Matematicamente, as camadas ocultas são expressas como as funcionalidades de entrada, multiplicadas por seus pesos associados e viés para passar de uma camada para a próxima camada, chegando finalmente à camada de saída. É aqui que a **transformação linear** entre a entrada e a saída acontece.   
      
    
- **Camada de saída**: após realizar a transformação linear na camada oculta, uma função de ativação não linear (tanh, sigmoide, ReLU ) é adicionada para produzir a previsão final (como um número para regressão ou uma distribuição de probabilidade para classificação).

Site tirado: [O que é uma rede neural? | IBM](https://www.ibm.com/br-pt/think/topics/neural-networks)
