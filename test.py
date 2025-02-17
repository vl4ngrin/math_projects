import sys

def file_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip() != '']

    # Первая строка
    nv_ne = lines[0].split()
    NV = int(nv_ne[0])
    NE = int(nv_ne[1])

    # NE - список ребёр
    edge_lines = lines[1:1+NE]
    edges = []
    for line in edge_lines:
        tim = line.split()
        src = int(tim[0])
        dst = int(tim[1])
        edges.append((src, dst))

    # Правила агент-функции (сначала для узлов, затем для ребёр)
    agent_lines = lines[1+NE:]
    vertex_agent = agent_lines[:NV]
    edge_agent = agent_lines[NV:]

    return NV, NE, edges, vertex_agent, edge_agent

# Вычисление атрибутов для узлов и ребёр

def evaluate_atributes(NV, NE, edges, vertex_agent, edge_agent):
    vertex_atr = {i: None for i in range(1, NV+1)}
    edge_atr = {i: None for i in range(1, NE+1)}

    # Создание словаря, в котором будет храниться список ребёр для каждого узла
    input_edges = {i: [] for i in range(1, NV+1)}
    for idx, (src, dst) in enumerate(edges, start=1):
        input_edges[dst].append(idx)

    changed = True
    while changed:
        changed = False

        # Вычисление правил для узлов NV
        for i in range (1, NV+1):
            if vertex_atr[i] is None:
                rule = vertex_agent[i-1]

                # Преобразование строки в число для 1-го правила
                try:
                  val = float(rule)
                  vertex_atr[i] = val
                  changed = True
                except ValueError:
                  pass

                # Если правило "буква число"
                parts = rule.split()
                if len(parts) == 2:
                  letter = parts[0]
                  ref = int(parts[1])
                  if letter == 'e':
                    if ref in edge_atr and edge_atr[ref] is not None:
                      vertex_atr[i] = edge_atr[ref]
                      changed = True 
                      continue
                  elif letter == 'v':
                    if ref in vertex_atr and vertex_atr[ref] is not None:
                      vertex_atr[i] = vertex_atr[ref]
                      changed = True
                      continue

                 # Если правило - min
                if rule == 'min':
                  if len(input_edges[i]) == 0:
                    continue
                  ready = True
                  values = []
                  for edge in input_edges[i]:
                    if edge_atr[edge] is None:
                      ready = False
                      break
                    values.append(edge_atr[edge])
                  if ready:
                    vertex_atr[i] = min(values)
                    changed = True
                    continue

        # Вычисление правил для ребёр NE
        for i in range(1, NE+1):
          if edge_atr[i] is None:
            rule = edge_agent[i-1]

            try:
              val = float(rule)
              edge_atr[i] = val
              changed = True
              continue
            except ValueError:
              pass

            parts = rule.split()
            if len(parts) == 2:
              letter = parts[0]
              ref = int(parts[1])
              if letter == 'e':
                if ref in edge_atr and edge_atr[ref] is not None:
                  edge_atr[i] = edge_atr[ref]
                  changed = True
                  continue
              elif letter == 'v':
                if ref in vertex_atr and vertex_atr[ref] is not None:
                  edge_atr[i] = vertex_atr[ref]
                  changed = True
                  continue

            if rule == '*':
              # Определение начального узла для ребра
              src = edges[i-1][0]
              if vertex_atr[src] is None:
                continue
              inp = input_edges[src]
              prod = 1.0
              ready = True
              for edge in inp:
                if edge_atr[edge] is None:
                  ready = False
                  break
                prod *= edge_atr[edge]
              if ready:
                edge_atr[i] = vertex_atr[src] * prod
                changed = True
                continue

    return vertex_atr, edge_atr

# Запись в файл
def write_output(filename, vertex_atr, edge_atr, NV, NE):
  with open(filename, 'w') as f:
        # Атрибуты узлов (каждый на отдельной строке)
    for i in range(1, NV+1):
      f.write(str(vertex_atr[i]) + "\n")
        # Атрибуты рёбер
    for i in range(1, NE+1):
      f.write(str(edge_atr[i]) + "\n")

def main():
    input_file = "input.txt"  
    output_file = "output.txt" 
    NV, NE, edges, vertex_agent, edge_agent = file_input(input_file)
    vertex_atr, edge_atr = evaluate_atributes(NV, NE, edges, vertex_agent, edge_agent)
    write_output(output_file, vertex_atr, edge_atr, NV, NE)

if __name__ == "__main__":
    main()
