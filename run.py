# Not adding shebang at this point as each of us will have different python
# directories

import os
from FAS import app


port = int(os.environ.get("PORT", 33507))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=port)