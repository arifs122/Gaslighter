// @category Gaslighter

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import java.io.FileWriter;

// Cagri: -postScript ExportC.java <out_json>
// Tum (CRT disi) fonksiyonlari decompile edip JSON listesi yazar:
//   [{"offset": "...", "name": "...", "c_code": "..."}, ...]
public class ExportC extends GhidraScript {

    static String esc(String s) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': b.append("\\\\"); break;
                case '"':  b.append("\\\""); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:   b.append(c);
            }
        }
        return b.toString();
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String out = (args.length > 0) ? args[0] : "/tmp/opencode/gaslighter_out.json";

        DecompInterface ifc = new DecompInterface();
        ifc.openProgram(currentProgram);

        StringBuilder sb = new StringBuilder("[\n");
        boolean first = true;
        int n = 0;
        FunctionManager fm = currentProgram.getFunctionManager();
        for (Function f : fm.getFunctions(true)) {
            if (f.isThunk() || f.isExternal()) continue;
            String nm = f.getName();
            if (nm.startsWith("_")) continue;          // _start/_init/_fini vb.
            DecompileResults res = ifc.decompileFunction(f, 60, monitor);
            if (res == null || !res.decompileCompleted()) continue;
            String c = res.getDecompiledFunction().getC();
            if (!first) sb.append(",\n");
            first = false;
            sb.append("{\"offset\":\"").append(esc(f.getEntryPoint().toString()))
              .append("\",\"name\":\"").append(esc(nm))
              .append("\",\"c_code\":\"").append(esc(c)).append("\"}");
            n++;
        }
        sb.append("\n]\n");
        try (FileWriter w = new FileWriter(out)) {
            w.write(sb.toString());
        }
        ifc.dispose();
        println("[ExportC] " + n + " fonksiyon yazildi: " + out);
    }
}
